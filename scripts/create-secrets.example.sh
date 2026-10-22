#!/usr/bin/env bash
set -euo pipefail
# Example of local secret creation; run AFTER configuring kubectl context.
# This script never writes actual credentials to Git.
# Set secrets locally using an ignored file containing KEY=VALUE lines.
NAMESPACE="${1:?Usage: bash scripts/create-secrets.example.sh liora-dev|liora-prod}"
case "$NAMESPACE" in
  liora-dev|liora-prod) ;;
  *) echo "Unknown namespace"; exit 1 ;;
esac
SECRETS_FILE=".secrets/${NAMESPACE}.env"
if [[ ! -f "$SECRETS_FILE" ]]; then
  echo "Create $SECRETS_FILE with POSTGRES_PASSWORD, SECRET_KEY, FIRST_SUPERUSER, FIRST_SUPERUSER_PASSWORD."
  exit 1
fi
kubectl create namespace "$NAMESPACE" --dry-run=client -o yaml | kubectl apply -f -
kubectl -n "$NAMESPACE" create secret generic course-app-secrets --from-env-file="$SECRETS_FILE" --dry-run=client -o yaml | kubectl apply -f -
echo "Created namespace-scoped application credentials; see docs/deployment.md for registry authentication."
