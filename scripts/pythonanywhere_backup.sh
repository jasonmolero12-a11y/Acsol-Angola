#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${PROJECT_DIR:-$HOME/Acsol-Angola}"
BACKUP_DIR="${BACKUP_DIR:-$HOME/acsol_backups}"
STAMP="$(date +%Y%m%d_%H%M%S)"

mkdir -p "$BACKUP_DIR"

if [ -f "$PROJECT_DIR/db.sqlite3" ]; then
  cp "$PROJECT_DIR/db.sqlite3" "$BACKUP_DIR/db_${STAMP}.sqlite3"
fi

if [ -d "$PROJECT_DIR/media" ]; then
  tar -czf "$BACKUP_DIR/media_${STAMP}.tar.gz" -C "$PROJECT_DIR" media
fi

find "$BACKUP_DIR" -type f -mtime +30 -delete

echo "Backup ACSOL concluido em $BACKUP_DIR"
