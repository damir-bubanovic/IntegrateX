#!/usr/bin/env sh
set -e

cd /app

echo "[entrypoint] DJANGO_ENV=${DJANGO_ENV:-dev}"
echo "[entrypoint] RUN_MIGRATIONS=${RUN_MIGRATIONS:-0}"
echo "[entrypoint] RUN_COLLECTSTATIC=${RUN_COLLECTSTATIC:-0}"

# Wait for Postgres if configured
if [ "${DB_ENGINE:-django.db.backends.sqlite3}" != "django.db.backends.sqlite3" ]; then
  echo "[entrypoint] Waiting for database ${DB_HOST:-db}:${DB_PORT:-5432}..."
  until python -c "import os, socket; s=socket.socket(); s.settimeout(1); s.connect((os.getenv('DB_HOST','db'), int(os.getenv('DB_PORT','5432')))); s.close()" 2>/dev/null; do
    sleep 1
  done
  echo "[entrypoint] Database is reachable."
fi

# Run migrations only when explicitly enabled (avoid concurrent migration races)
if [ "${RUN_MIGRATIONS:-0}" = "1" ]; then
  echo "[entrypoint] Running migrations..."
  python manage.py migrate --noinput
fi

# Collect static only when explicitly enabled
if [ "${RUN_COLLECTSTATIC:-0}" = "1" ]; then
  echo "[entrypoint] Collecting static..."
  python manage.py collectstatic --noinput
fi

echo "[entrypoint] Starting: $*"
exec "$@"
