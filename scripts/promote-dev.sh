#!/usr/bin/env bash
set -euo pipefail
# Call only after SOURCE_SHA's images have passed the publication gates.
SOURCE_SHA="${1:?Usage: promote-dev.sh FULL_VALIDATED_SHA [--push]}"
PUSH="${2:-}"
[[ "$SOURCE_SHA" =~ ^[0-9a-f]{40}$ ]] || { echo 'Expected a full commit SHA' >&2; exit 1; }
[[ -z "$PUSH" || "$PUSH" == --push ]] || { echo 'Unknown option' >&2; exit 1; }
[[ -z "$(git status --porcelain)" ]] || { echo 'Refusing a dirty checkout' >&2; exit 1; }
git cat-file -e "$SOURCE_SHA^{commit}"
MANIFEST=kubernetes/overlays/dev/kustomization.yaml
if git ls-remote --exit-code --heads origin deploy/dev >/dev/null; then
  git fetch origin refs/heads/deploy/dev:refs/remotes/origin/deploy/dev
  git switch -c deploy/dev refs/remotes/origin/deploy/dev
  BEFORE="$(git rev-parse HEAD)"
  BASE="$(git merge-base HEAD "$SOURCE_SHA")"
  if ! git merge --no-edit "$SOURCE_SHA"; then
    CONFLICTS="$(git diff --name-only --diff-filter=U)"
    if [[ "$CONFLICTS" != "$MANIFEST" ]]; then
      git merge --abort
      echo 'Unexpected promotion conflict; manual review required' >&2
      exit 1
    fi
    # Only generated image-tag edits may be superseded by the validated source.
    # Other dev edits must never be silently overwritten, including on this file.
    if ! python3 - "$BASE" "$BEFORE" "$MANIFEST" <<'PY'
import re
import subprocess
import sys

patch = subprocess.check_output([
    "git", "diff", "--no-ext-diff", "--unified=0", sys.argv[1], sys.argv[2], "--", sys.argv[3],
], text=True)
changes = [line for line in patch.splitlines()
           if line.startswith(("+", "-")) and not line.startswith(("+++", "---"))]
if not changes or not all(re.fullmatch(r"[+-]\s*newTag: sha-[a-z0-9]+", line) for line in changes):
    raise SystemExit("Dev manifest contains non-generated edits; refusing automatic conflict resolution")
PY
    then
      git merge --abort
      exit 1
    fi
    git checkout "$SOURCE_SHA" -- "$MANIFEST"
    git add "$MANIFEST"
    git commit --no-edit
    echo 'Resolved only generated image-tag conflict; validated manifest retained'
  fi
else
  git switch -c deploy/dev "$SOURCE_SHA"
fi
python3 - "$MANIFEST" "$SOURCE_SHA" <<'PY'
from pathlib import Path
import re
import sys

path = Path(sys.argv[1])
text, count = re.subn(r"(newTag: )sha-[a-z0-9]+", r"\g<1>sha-" + sys.argv[2], path.read_text())
if count != 2:
    raise SystemExit("Expected exactly the backend and frontend image tags")
path.write_text(text)
PY
git add "$MANIFEST"
if ! git diff --cached --quiet; then
  git commit -m "chore(gitops): promote scanned dev images to sha-$SOURCE_SHA"
fi
if [[ "$PUSH" == --push ]]; then
  git push origin HEAD:refs/heads/deploy/dev
else
  echo 'Prepared development promotion; review before an explicit push'
fi
