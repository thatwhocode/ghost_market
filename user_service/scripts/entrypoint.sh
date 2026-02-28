#!/bin/bash

# Зупинити виконання при помилці
set -e

echo "Waiting for PostgreSQL at ${POSTGRES_PORT}..."

python << END
import socket
import time
import os

# Використовуємо саме твої назви з .env
db_host = os.getenv("POSTGRES_HOST", "db")
db_port = int(os.getenv("POSTGRES_PORT", 5432))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    try:
        s.connect((db_host, db_port))
        s.close()
        break
    except socket.error:
        print(f"Waiting for database on port {db_port}...")
        time.sleep(1)
END

echo "PostgreSQL is up - executing migrations"
cd /app/user_service
# Виконуємо міграції
alembic upgrade head

echo "Migrations completed - starting FastAPI on port ${API_PORT}"

# Використовуємо API_PORT з .env для запуску uvicorn
exec uvicorn user_service.main:app --host 0.0.0.0 --port ${CONTAINER_PORT:-8000}