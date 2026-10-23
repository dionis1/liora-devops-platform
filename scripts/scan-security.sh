#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
TRIVY="${TRIVY_BIN:-trivy}"
STATUS=0
# Scan every patched application dependency, including development dependencies.
"$TRIVY" fs --parallel 1 --include-dev-deps --scanners vuln,secret \
  --severity HIGH,CRITICAL --exit-code 1 \
  --skip-dirs course-app/backend/.venv --skip-dirs course-app/backend/htmlcov \
  --skip-dirs course-app/frontend/node_modules course-app || STATUS=1
# Configuration scope is the actual platform deployment, not unused upstream
# development Dockerfiles/Compose examples. No vulnerability IDs are suppressed.
for TARGET in docker kubernetes infrastructure; do
  "$TRIVY" config --severity HIGH,CRITICAL --exit-code 1 \
    --skip-dirs infrastructure/terraform/.terraform "$TARGET" || STATUS=1
done
"$TRIVY" fs --scanners secret --severity HIGH,CRITICAL --exit-code 1 \
  --skip-dirs .git --skip-dirs course-app/backend/.venv \
  --skip-dirs course-app/frontend/node_modules \
  --skip-dirs infrastructure/terraform/.terraform \
  --skip-dirs docs/local-validation-evidence \
  --skip-dirs docs/remediation-evidence . || STATUS=1
exit "$STATUS"
