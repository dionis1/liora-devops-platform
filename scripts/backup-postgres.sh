#!/usr/bin/env bash
# Save a compressed PostgreSQL backup OUTSIDE the Kubernetes node.
set -euo pipefail
NAMESPACE="${1:?Usage: bash scripts/backup-postgres.sh liora-dev|liora-prod}"
case "$NAMESPACE" in
  liora-dev|liora-prod) ;;
  *) echo "Invalid namespace"; exit 1 ;;
esac
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEST="${BACKUP_DIR:-$ROOT/.secrets/backups}"
umask 077
mkdir -p "$DEST"
TEMP="$(mktemp "$DEST/${NAMESPACE}-$(date -u +%Y%m%dT%H%M%SZ).XXXXXX.tmp")"
FILE="${TEMP%.tmp}.dump"
trap 'rm -f -- "$TEMP"' EXIT
kubectl -n "$NAMESPACE" exec postgres-0 -- pg_dump -U app -d app -Fc > "$TEMP"
test -s "$TEMP"
# Publish only a successful dump, atomically, without replacing another backup.
ln -- "$TEMP" "$FILE"
echo "Backup saved to $FILE (copy to offline/encrypted storage)"
