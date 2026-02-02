#!/bin/bash
set -e

echo "Waiting for DB Orders..."

# подключаемся в базу (стучимся)
until pg_isready -h "$POSTGRES_ORDERS_HOST" \
                 -p "$POSTGRES_ORDERS_PORT" \
                 -U "$POSTGRES_USER_ORDERS"; do
    echo "Postgres_ORDERS not ready, sleeping..."
    sleep 1
done

echo "Postgres_ORDERS is ready, running migrations... by uv in virtual env"


# теперь запускаем Alembic через бинарник из виртуалки для миграции
/order/.venv/bin/alembic upgrade head

echo "Starting API Orders..."
exec "$@"