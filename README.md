# E-Commerce Backend — FastAPI + SQLAlchemy + Kafka

Microservice-based e-commerce backend with event-driven order processing
and domain-driven service separation.

## Overview

This project demonstrates a production-style backend architecture
where services are independently deployable, communicate asynchronously
via Kafka, and each own their own database schema.

## Services

| Service   | Responsibility                                          |
|-----------|---------------------------------------------------------|
| `user`    | Registration, JWT authentication, role-based access     |
| `product` | Product catalog — CRUD operations                       |
| `cart`    | Cart management, item aggregation                       |
| `order`   | Order lifecycle management + Kafka event publishing     |

## Tech Stack

| Layer          | Technology                        |
|----------------|-----------------------------------|
| Framework      | FastAPI, Pydantic                 |
| ORM            | SQLAlchemy 2.0                    |
| Migrations     | Alembic                           |
| Database       | PostgreSQL                        |
| Messaging      | Kafka                             |
| Infrastructure | Docker, Docker Compose            |
| Scripts        | Shell — automated migration runner|

## Project Structure
```
├── user/
│   ├── models.py
│   ├── router.py
│   └── schemas.py
├── product/
├── cart/
├── order/
├── docker-compose.yaml
└── README.md
```

## Run Locally
```bash
docker-compose up --build
```

Alembic migrations run automatically on container startup via shell scripts.
No manual migration steps required.

## API Endpoints (examples)

| Method | Endpoint              | Description          |
|--------|-----------------------|----------------------|
| POST   | `/user/register`      | Register new user    |
| POST   | `/user/login`         | Get JWT token        |
| GET    | `/product/`           | List products        |
| POST   | `/cart/add`           | Add item to cart     |
| POST   | `/order/create`       | Create order + publish Kafka event |

## Key Design Decisions

**Domain separation** — each service owns its DB models independently.
Cross-service calls go through APIs, not shared ORM models.

**Kafka for async processing** — order creation publishes an event to Kafka,
decoupling the order service from any downstream consumers (notifications,
inventory updates, etc).

**Automated migrations** — Alembic runs on container startup via shell scripts,
making fresh deployments and CI environments require zero manual steps.

**SQLAlchemy 2.0** — uses the modern `select()` style throughout,
not legacy Query API.