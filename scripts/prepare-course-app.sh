#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SOURCE="$ROOT/course-app"
PATCH="$ROOT/patches/course-app-platform.patch"
EXPECTED="$(git -C "$ROOT" rev-parse HEAD:course-app)"
ACTUAL="$(git -C "$SOURCE" rev-parse HEAD)"
if [[ "$ACTUAL" != "$EXPECTED" ]]; then
  echo "Submodule revision differs from the pinned gitlink; review the patch before applying." >&2
  exit 1
fi
if git -C "$SOURCE" apply --reverse --check "$PATCH" >/dev/null 2>&1; then
  echo "Reviewed platform patch is already applied."
  exit 0
fi
if ! git -C "$SOURCE" diff --quiet || ! git -C "$SOURCE" diff --cached --quiet; then
  echo "Submodule has local edits; preserve and review them before applying the platform patch." >&2
  exit 1
fi
git -C "$SOURCE" apply --check "$PATCH"
git -C "$SOURCE" apply "$PATCH"
echo "Applied the reviewed dependency, compatibility and metrics patch to the original app."
