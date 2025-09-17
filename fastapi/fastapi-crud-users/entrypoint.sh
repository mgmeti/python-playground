#!/bin/sh

echo "⏳ Waiting for Postgres to be ready..."

# Run a short Python script to wait for DB
python - <<END
import os
import time
import psycopg2
from psycopg2 import OperationalError

host = os.getenv("POSTGRES_HOST", "postgres")
port = int(os.getenv("POSTGRES_PORT", 5432))
db = os.getenv("POSTGRES_DB", "users_db")
user = os.getenv("POSTGRES_USER", "postgres")
password = os.getenv("POSTGRES_PASSWORD", "postgres")

while True:
    try:
        conn = psycopg2.connect(host=host, port=port, dbname=db, user=user, password=password)
        conn.close()
        break
    except OperationalError:
        time.sleep(1)
END

echo "✅ Postgres is up - running migrations..."

# Run Alembic migrations
alembic upgrade head

echo "🚀 Starting FastAPI..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
