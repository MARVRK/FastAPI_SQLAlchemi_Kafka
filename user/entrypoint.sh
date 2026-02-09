#!/bin/bash
set -e

echo "Waiting for DB USERS..."

# подключаемся в базу (стучимся)
until pg_isready -h "$POSTGRES_USERS_HOST" \
                 -p "$POSTGRES_USERS_PORT" \
                 -U "$POSTGRES_USER_USERS"; do
    echo "Postgres_USERS not ready, sleeping..."
    sleep 1
done

echo "Postgres_USERS is ready, running migrations... by uv in virtual env"


# теперь запускаем Alembic через бинарник из виртуалки для миграции
/users/.venv/bin/alembic upgrade head

echo "Starting API USERS..."
exec "$@"