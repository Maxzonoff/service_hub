#!/usr/bin/env bash
# ─────────────────────────────────────────────
# entrypoint.sh — что делать при старте контейнера:
# 1. Ждать PostgreSQL
# 2. Применить миграции
# 3. Собрать статику
# 4. Запустить переданную команду (gunicorn)
# ─────────────────────────────────────────────
set -e

echo "⏳ Ожидаем PostgreSQL на ${POSTGRES_HOST}:${POSTGRES_PORT}..."
while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  sleep 1
done
echo "✅ PostgreSQL доступен"

echo "⏳ Применяем миграции..."
python manage.py migrate --noinput

echo "⏳ Собираем статику..."
python manage.py collectstatic --noinput

echo "🚀 Запуск: $@"
exec "$@"