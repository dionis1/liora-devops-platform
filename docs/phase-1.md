# Phase 1: Adopt the course application and establish GitHub Actions CI

## Why the application changed

The course assigns an existing application, [DataScientest FastAPI + Traefik](https://github.com/DataScientest/fastapi-traefik-datascientest-project). An earlier custom TaskFlow demo was an incorrect choice and has been removed in this change. The source stays pinned at a known upstream commit using a Git submodule.

## Clone the complete project

```bash
git clone --recurse-submodules https://github.com/dionis1/liora-devops-platform.git
cd liora-devops-platform
git submodule status
```

Existing local clones:

```bash
git pull --ff-only
git submodule update --init --recursive
```

The Git submodule contents appear in `course-app/`. A normal `git clone` without `--recurse-submodules` does **not** populate them.

## Local application

Prerequisites: Docker Engine with Compose plugin, suitable free ports and disk capacity.

```bash
cd course-app
docker compose build
docker compose up -d --wait backend frontend
curl -fsS http://localhost:8000/api/v1/utils/health-check/
docker compose down
```

The original app includes PostgreSQL and a React frontend. Do not copy the upstream `.env` placeholder secrets into production.

## GitHub Actions workflow

The root `.github/workflows/ci.yml` checks out submodules and runs original backend linting, migrations, PostgreSQL-dependent pytest tests, and Docker image builds. Once code is merged into `main`, passing builds publish to:

- `ghcr.io/dionis1/liora-devops-platform-backend:sha-<commit>`
- `ghcr.io/dionis1/liora-devops-platform-frontend:sha-<commit>`

Package visibility may remain private, requiring an image pull secret when deploying k3s. The built frontend currently expects a same-origin `/api` ingress route in the future Kubernetes setup.

Inspect status under GitHub > Actions. Do not merge a PR with failing checks. On private repositories check the settings for workflow permissions and GitHub-hosted runners.

## Limitations and next phase

- CI builds and publishes but does not deploy to k3s yet. Argo CD will handle CD.
- Upstream submodule is pinned intentionally: update with a reviewed PR, do not blindly follow main.
- No real production credentials have been configured; Kubernetes Secrets and recovery come later.
- Harden upstream images and add dependency/image scanning before calling the system production-ready.
