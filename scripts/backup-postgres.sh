#!/usr/bin/env bash
# Save a compressed PostgreSQL backup OUTSIDE the Kubernetes node.
set -euo pipefail
NAMESPACE="${1:?Usage: bash scripts/backup-postgres.sh liora-dev|liora-prod}"
case "$NAMESPACE" in
  liora-dev|liora-prod) ;;
  *) echo "Invalid namespace"; exit 1 ;;
esac
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEST="$ROOT/.secrets/backups"
mkdir -p "$DEST"
umask 077
FILE="$DEST/${NAMESPACE}-$(date -u +%Y%m%dT%H%M%SZ).dump"
kubectl -n "$NAMESPACE" exec postgres-0 -- pg_dump -U app -d app -Fc > "$FILE"
test -s "$FILE"
echo "Backup saved to $FILE (copy to offline/encrypted storage)"
