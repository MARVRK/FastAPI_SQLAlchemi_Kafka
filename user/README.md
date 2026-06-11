# User Service

Manages users, authentication, and authorization via JWT + refresh tokens.

## Stack

| Layer      | Technology              |
|------------|-------------------------|
| Framework  | FastAPI                 |
| ORM        | SQLAlchemy 2.0 (async)  |
| Migrations | Alembic                 |
| Database   | PostgreSQL              |
| Validation | Pydantic v2             |
| Auth       | PyJWT + bcrypt          |

## Structure

```
user/
├── api/            # Route handlers
│   └── user.py
├── dependencies/   # FastAPI dependency injection
│   └── core.py
├── error/          # Custom exceptions
│   └── error.py
├── infra/          # DB engine, session, settings
│   ├── base.py
│   └── settings.py
├── models/         # SQLAlchemy ORM models
│   └── user.py     # User, RefreshToken
├── repositories/   # DB queries (abstraction + implementation)
│   └── user_repo.py  # UserRepository, RefreshTokenRepository
├── schemas/        # Pydantic schemas
│   ├── requests.py   # UserRegister, UserLogin, UserUpdate
│   └── responses.py  # UserResponse, TokenResponse
├── services/       # Business logic
│   └── user_service.py
├── utils/          # JWT and password helpers
│   └── jwt.py
├── alembic/        # Migrations
└── main.py         # App entry point + exception handlers
```

## API

| Method  | Endpoint                       | Auth | Description                           |
|---------|--------------------------------|------|---------------------------------------|
| `POST`  | `/user/register`               | —    | Register new user                     |
| `POST`  | `/user/login`                  | —    | Login, returns access + refresh token |
| `POST`  | `/user/refresh-access-token`   | —    | Get new access token via refresh token|
| `POST`  | `/user/logout`                 | —    | Revoke refresh token                  |
| `GET`   | `/user/me`                     | JWT  | Get current user info                 |
| `PATCH` | `/user/{user_id}`              | JWT  | Update user role or active status     |

## Auth Flow

```
POST /login
  → bcrypt verify password
  → revoke all existing refresh tokens
  → create access_token (JWT, 30 min)
  → create refresh_token (UUID, 30 days) → save to DB
  → return both to client

client stores both tokens

access_token expired → 401
  → client sends refresh_token to POST /refresh-access-token
  → old refresh_token revoked, new one issued
  → client retries with new access_token

refresh_token expired/revoked → 401
  → client redirects to login
```

## Token Design

| Token         | Type | Storage        | Lifetime | Stateful |
|---------------|------|----------------|----------|----------|
| access_token  | JWT  | client         | 30 min   | No       |
| refresh_token | UUID | DB + client    | 30 days  | Yes      |

Access token is stateless — validated by decoding JWT signature, no DB lookup.
Refresh token is stateful — stored in DB, can be revoked at any time.
One active refresh token per user — revoked on each new login.

## Error Handling

| Exception                   | Status | Message                        |
|-----------------------------|--------|--------------------------------|
| `UserError`                 | 404    | User not found / no fields     |
| `AuthError`                 | 401    | Invalid credentials / token    |
| `IntegrityError`            | 409    | Email already exists           |
| `jwt.ExpiredSignatureError` | 401    | Token expired                  |
| `jwt.InvalidTokenError`     | 401    | Invalid token                  |

## Dependency Flow

```
Request
  └── Depends(get_user_service)
        └── UserService(
              user_repo=UserRepository(),
              token_repo=RefreshTokenRepository(),
              db=AsyncSession
            )

Protected endpoints additionally:
  └── Depends(get_current_user)
        └── decode_access_token(Bearer token) → payload dict
```

## Migrations

Alembic runs automatically on container startup via `entrypoint.sh`.
