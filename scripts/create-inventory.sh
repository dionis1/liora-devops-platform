#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
IP="$(cd "$ROOT/infrastructure/terraform" && terraform output -raw server_public_ipv4)"
mkdir -p "$ROOT/ansible/inventory"
printf '[k3s_servers]\nk3s-01 ansible_host=%s ansible_user=root\n' "$IP" > "$ROOT/ansible/inventory/hosts.ini"
echo "Created ansible/inventory/hosts.ini (ignored by Git)."
