#!/bin/bash
set -e

echo "Waiting for DB Products..."

# подключаемся в базу (стучимся)
until pg_isready -h "$POSTGRES_PRODUCTS_HOST" \
                 -p "$POSTGRES_PRODUCTS_PORT" \
                 -U "$POSTGRES_USER_PRODUCTS"; do
    echo "Postgres_PRODUCTS not ready, sleeping..."
    sleep 1
done

echo  "Postgres_ORDERS is ready, running migrations... by virtual env and alembic"


# теперь запускаем Alembic через бинарник из виртуалки для миграции
/product/.venv/bin/alembic upgrade head

echo "Starting API Products..."
exec "$@"