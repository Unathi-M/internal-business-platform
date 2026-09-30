import hashlib
import hmac
import os
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
import psycopg
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel


app = FastAPI(
    title="Internal Business Platform API",
    version="0.2.0",
    description="A local-only training application for authorized security testing.",
)

DATABASE_URL = os.environ["DATABASE_URL"]
JWT_SECRET = os.environ["JWT_SECRET"]
JWT_ALGORITHM = "HS256"
TOKEN_LIFETIME_MINUTES = 30

security = HTTPBearer(auto_error=False)


class LoginRequest(BaseModel):
    email: str
    password: str


class OrderCreate(BaseModel):
    customer_id: int | None = None
    description: str
    total_cents: int


def get_connection():
    return psycopg.connect(DATABASE_URL)


def hash_password(password: str, salt: bytes | None = None) -> str:
    """Create a scrypt password hash for local training use."""
    salt = salt or secrets.token_bytes(16)

    derived_key = hashlib.scrypt(
        password.encode("utf-8"),
        salt=salt,
        n=16_384,
        r=8,
        p=1,
        dklen=32,
    )

    return (
        "scrypt$16384$8$1$"
        f"{salt.hex()}$"
        f"{derived_key.hex()}"
    )


def verify_password(password: str, stored_hash: str) -> bool:
    """Verify a password against a stored local scrypt hash."""
    try:
        algorithm, n, r, p, salt_hex, expected_hex = stored_hash.split("$")

        if algorithm != "scrypt":
            return False

        derived_key = hashlib.scrypt(
            password.encode("utf-8"),
            salt=bytes.fromhex(salt_hex),
            n=int(n),
            r=int(r),
            p=int(p),
            dklen=32,
        )

        return hmac.compare_digest(
            derived_key.hex(),
            expected_hex,
        )
    except (ValueError, TypeError):
        return False


def create_access_token(user_id: int, email: str, role: str) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=TOKEN_LIFETIME_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "email": email,
        "role": role,
        "exp": expires_at,
    }

    return jwt.encode(
        payload,
        JWT_SECRET,
        algorithm=JWT_ALGORITHM,
    )


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> dict[str, Any]:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = jwt.decode(
            credentials.credentials,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM],
        )

        return {
            "id": int(payload["sub"]),
            "email": payload["email"],
            "role": payload["role"],
        }

    except (
        jwt.InvalidTokenError,
        KeyError,
        TypeError,
        ValueError,
    ) as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from error


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/v1/auth/login")
def login(login_request: LoginRequest) -> dict[str, str]:
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT id, email, password_hash, role
            FROM users
            WHERE email = %s
            """,
            (login_request.email,),
        ).fetchone()

    if row is None or not verify_password(
        login_request.password,
        row[2],
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_access_token(
        user_id=row[0],
        email=row[1],
        role=row[3],
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }


@app.get("/api/v1/me")
def current_user(
    user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    return user


@app.get("/api/v1/users")
def list_users(
    user: dict[str, Any] = Depends(get_current_user),
) -> list[dict[str, Any]]:
    if user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator role required",
        )

    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, email, role FROM users ORDER BY id"
        ).fetchall()

    return [
        {
            "id": row[0],
            "email": row[1],
            "role": row[2],
        }
        for row in rows
    ]


@app.get("/api/v1/orders")
def list_orders(
    user: dict[str, Any] = Depends(get_current_user),
) -> list[dict[str, Any]]:
    with get_connection() as conn:
        if user["role"] == "admin":
            rows = conn.execute(
                """
                SELECT id, customer_id, description, total_cents
                FROM orders
                ORDER BY id
                """
            ).fetchall()
        else:
            rows = conn.execute(
                """
                SELECT id, customer_id, description, total_cents
                FROM orders
                WHERE customer_id = %s
                ORDER BY id
                """,
                (user["id"],),
            ).fetchall()

    return [
        {
            "id": row[0],
            "customer_id": row[1],
            "description": row[2],
            "total_cents": row[3],
        }
        for row in rows
    ]


@app.get("/api/v1/orders/{order_id}")
def get_order(
    order_id: int,
    user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT id, customer_id, description, total_cents
            FROM orders
            WHERE id = %s
            """,
            (order_id,),
        ).fetchone()

    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    if user["role"] != "admin" and row[1] != user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot access this order",
        )

    return {
        "id": row[0],
        "customer_id": row[1],
        "description": row[2],
        "total_cents": row[3],
    }


@app.post("/api/v1/orders", status_code=201)
def create_order(
    order: OrderCreate,
    user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    if order.total_cents <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="total_cents must be positive",
        )

    customer_id = order.customer_id

    if user["role"] != "admin":
        customer_id = user["id"]

    if customer_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="customer_id is required for administrators",
        )

    with get_connection() as conn:
        row = conn.execute(
            """
            INSERT INTO orders (customer_id, description, total_cents)
            VALUES (%s, %s, %s)
            RETURNING id, customer_id, description, total_cents
            """,
            (
                customer_id,
                order.description,
                order.total_cents,
            ),
        ).fetchone()

        conn.commit()

    return {
        "id": row[0],
        "customer_id": row[1],
        "description": row[2],
        "total_cents": row[3],
    }
