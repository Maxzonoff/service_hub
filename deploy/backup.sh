#!/bin/bash
# ─────────────────────────────────────────────
# Скрипт резервного копирования БД Service Hub
# Запускается через cron ежедневно.
# Пример cron (crontab -e):
#   0 3 * * * /home/deploy/service_hub/deploy/backup.sh >> /home/deploy/backups/backup.log 2>&1
# ─────────────────────────────────────────────
set -e

BACKUP_DIR="/home/deploy/backups"
DB_NAME="service_hub"
DB_USER="service_hub"
DATE=$(date +%Y-%m-%d_%H-%M)

mkdir -p "$BACKUP_DIR"

# Создаём дамп
pg_dump -U "$DB_USER" -h localhost "$DB_NAME" > "$BACKUP_DIR/${DB_NAME}_${DATE}.sql"

# Сжимаем
gzip "$BACKUP_DIR/${DB_NAME}_${DATE}.sql"

# Удаляем бэкапы старше 30 дней
find "$BACKUP_DIR" -type f -name "*.sql.gz" -mtime +30 -delete

echo "[$(date +%Y-%m-%d\ %H:%M:%S)] Backup created: ${DB_NAME}_${DATE}.sql.gz"