# Product Service

Manages the product catalog. Provides full CRUD for products.

## Stack

| Layer      | Technology              |
|------------|-------------------------|
| Framework  | FastAPI                 |
| ORM        | SQLAlchemy 2.0 (async)  |
| Migrations | Alembic                 |
| Database   | PostgreSQL              |
| Validation | Pydantic v2             |

## Structure

```
product/
├── api/            # Route handlers
│   └── product.py
├── dependencies/   # FastAPI dependency injection
│   └── core.py
├── error/          # Custom exceptions
│   └── error.py
├── infra/          # DB engine, session, settings
│   ├── base.py
│   └── settings.py
├── models/         # SQLAlchemy ORM models
│   └── product.py
├── repositories/   # DB queries (abstraction + implementation)
│   └── product_repo.py
├── schemas/        # Pydantic schemas
│   ├── requests.py   # ProductCreate, ProductUpdate
│   └── responses.py  # ProductResponse
├── services/       # Business logic
│   └── product_service.py
├── alembic/        # Migrations
└── main.py         # App entry point + exception handlers
```

## API

| Method   | Endpoint              | Description         |
|----------|-----------------------|---------------------|
| `GET`    | `/product/`           | List all products   |
| `GET`    | `/product/{id}`       | Get product by id   |
| `POST`   | `/product/`           | Create product      |
| `PATCH`  | `/product/{id}`       | Partial update      |
| `DELETE` | `/product/{id}`       | Delete product      |

## Error Handling

Errors are handled globally in `main.py`:

| Exception        | Status | Message                          |
|------------------|--------|----------------------------------|
| `ProductError`   | 404    | Product not found                |
| `IntegrityError` | 409    | Product with this name already exists |

## Dependency Flow

```
Request
  └── Depends(get_product_service)
        └── ProductService(repo=ProductRepository(), db=AsyncSession)
```

## Migrations

Alembic runs automatically on container startup via `entrypoint.sh`.
