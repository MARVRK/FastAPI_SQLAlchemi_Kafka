#!/bin/bash
set -e

echo "Waiting for DB CART..."

# подключаемся в базу (стучимся)
until pg_isready -h "$POSTGRES_CART_HOST" \
                 -p "$POSTGRES_CART_PORT" \
                 -U "$POSTGRES_CART_CART"; do
    echo "Postgres_CART not ready, sleeping..."
    sleep 1
done

echo "Postgres_CART is ready, running migrations... by virtual env and alembic"


# теперь запускаем Alembic через бинарник из виртуалки для миграции
/cart/.venv/bin/alembic upgrade head

echo "Starting API CART..."
exec "$@"