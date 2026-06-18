#!/bin/sh
set -e

# Executa seed do usuário de teste (se o script existir)
if [ -f "/app/scripts/seed_test_user.py" ]; then
  echo "Running seed_test_user.py..."
  python /app/scripts/seed_test_user.py || true
else
  echo "No seed script found. Skipping."
fi

echo "Starting Uvicorn..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
