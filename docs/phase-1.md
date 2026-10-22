# Phase 1 - GitHub Actions CI and local development

## Clone the repository

```bash
git clone https://github.com/dionis1/liora-devops-platform.git
cd liora-devops-platform
```

This repository is private. Sign into GitHub when prompted, or use `gh auth login` and `gh auth setup-git` beforehand. Never paste access tokens into source files.

## Run locally (Ubuntu)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
ruff check app tests
python -m pytest -q
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs to try the API.

## Build and run with Docker

```bash
docker build -t taskflow-api:local .
docker run --rm -p 8000:8000 taskflow-api:local
```

Try `curl http://localhost:8000/health/live`.

## CI workflow

`.github/workflows/ci.yml` runs on PRs and pushes to `main` and can be started manually. It checks out the code, installs pinned dependencies, runs Ruff and pytest, and builds the Docker image. A successful push to main also authenticates with `GITHUB_TOKEN` and publishes a SHA-tagged image to GitHub Container Registry:

```text
ghcr.io/dionis1/liora-devops-platform:sha-<full-git-commit-sha>
```

Look for status under **GitHub repository > Actions > CI - Test and Docker**. If the repository is private, the GHCR package may also be private; Kubernetes image pull credentials will be configured in a later phase.

## Deliberate Phase 1 limitations

- Tasks are in memory, so a restart erases them; PostgreSQL and migrations come next.
- Readiness only checks the web process until PostgreSQL is integrated.
- This phase provides CI and image publishing, not a live Kubernetes deployment; Argo CD CD comes later.
- Before production use: upgrade from action version tags to pinned commit SHAs, enforce branch protection, add image/dependency scanning, restrict permissions, and deploy persistent storage.
