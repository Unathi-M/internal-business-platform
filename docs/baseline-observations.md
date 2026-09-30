# Baseline API Observations

## Environment

- Target: http://127.0.0.1:8080
- Environment: Local Docker lab
- Data: Synthetic data only
- Date:
- Tester: Project owner

## Confirmed endpoints

| Method | Endpoint | Purpose | Status |
|---|---|---|---|
| GET | /health | Health check | Tested |
| GET | /api/v1/users | List users | Tested |
| GET | /api/v1/orders | List orders | Tested |
| POST | /api/v1/orders | Create order | Tested |

## Initial observations

1. The API is accessible through the local Nginx reverse proxy.
2. The API currently has no authentication mechanism.
3. User records include email addresses and roles.
4. Order records include customer IDs and financial values.
5. The API accepts new orders using a JSON request body.
6. All data is synthetic and local to the Docker lab.

## Current limitations

- Authentication has not yet been implemented.
- Authorization testing has not yet been performed.
- No security headers have been assessed.
- No rate-limit testing has been performed.
- No source-code or dependency scan has been performed.
- These observations are baseline behavior, not confirmed vulnerabilities.

## Evidence

- Swagger UI: http://localhost:8080/docs
- Health check: http://localhost:8080/health
