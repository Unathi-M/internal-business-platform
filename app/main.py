import os
from typing import Any

import psycopg
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI(
    title="Internal Business Platform API",
    version="0.1.0",
    description="A local-only training application for authorized security testing.",
)

DATABASE_URL = os.environ["DATABASE_URL"]


class OrderCreate(BaseModel):
    customer_id: int
    description: str
    total_cents: int


def get_connection():
    return psycopg.connect(DATABASE_URL)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/v1/users")
def list_users() -> list[dict[str, Any]]:
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
def list_orders() -> list[dict[str, Any]]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, customer_id, description, total_cents "
            "FROM orders ORDER BY id"
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


@app.post("/api/v1/orders", status_code=201)
def create_order(order: OrderCreate) -> dict[str, Any]:
    if order.total_cents <= 0:
        raise HTTPException(
            status_code=400,
            detail="total_cents must be positive",
        )

    with get_connection() as conn:
        row = conn.execute(
            "INSERT INTO orders "
            "(customer_id, description, total_cents) "
            "VALUES (%s, %s, %s) "
            "RETURNING id, customer_id, description, total_cents",
            (
                order.customer_id,
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
