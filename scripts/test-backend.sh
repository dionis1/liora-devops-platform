#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
bash "$ROOT/scripts/prepare-course-app.sh"
umask 077
WORK="$(mktemp -d)"
PROJECT="liora-test-${RANDOM}-${RANDOM}"
export POSTGRES_USER=app POSTGRES_DB=app POSTGRES_SERVER=127.0.0.1
export POSTGRES_PORT="${LOCAL_TEST_PORT:-15432}"
export POSTGRES_PASSWORD="$(openssl rand -hex 24)"
export SECRET_KEY="$(openssl rand -hex 32)"
export FIRST_SUPERUSER=validation@example.com
export FIRST_SUPERUSER_PASSWORD="$(openssl rand -hex 16)"
export PROJECT_NAME=Local-validation ENVIRONMENT=local
export SMTP_HOST=smtp.invalid SMTP_PORT=1025 SMTP_TLS=false
export EMAILS_FROM_EMAIL=noreply@example.com
COMPOSE=(docker compose -p "$PROJECT" -f "$ROOT/tests/docker-compose.backend.yml")
cleanup() {
  "${COMPOSE[@]}" down --timeout 10
  rm -rf -- "$WORK"
}
trap cleanup EXIT
"${COMPOSE[@]}" up -d --wait --wait-timeout 90 db
cd "$ROOT/course-app/backend"
uv sync --frozen --python 3.12
uv run --frozen bash scripts/prestart.sh
uv run --frozen bash scripts/tests-start.sh
cd "$ROOT"
uv run --project course-app/backend --frozen python -m pytest tests/test_platform_metrics.py -q
