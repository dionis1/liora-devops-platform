# Liora DevOps Platform

Infrastructure and CI/CD project for the **DataScientest FastAPI + Traefik application**.

**Application source:** [DataScientest/fastapi-traefik-datascientest-project](https://github.com/DataScientest/fastapi-traefik-datascientest-project) (MIT License). The course application is tracked as a Git submodule at `course-app/`, pinned to a reviewed commit. We are not developing a different API.

## Application components

- FastAPI backend (Python, SQLModel, PostgreSQL, Alembic, pytest)
- React + TypeScript frontend
- Traefik reverse proxy and Docker Compose for local development
- GitHub Actions: backend lint and tests, Docker build, and GHCR publication on main
- Planned DevOps work: Terraform, Ansible, k3s, Argo CD, Prometheus, Grafana, security and backups

## Clone, including application

```bash
git clone --recurse-submodules https://github.com/dionis1/liora-devops-platform.git
cd liora-devops-platform
git submodule status
```

If already cloned: `git pull --ff-only && git submodule update --init --recursive`.

## Run the original application

```bash
cd course-app
docker compose build
docker compose up -d --wait backend frontend
```

The original template's development environment uses `course-app/.env` containing **example-only credentials**. Never use those unchanged in a publicly accessible deployment.

- Backend interactive API: http://localhost:8000/docs
- Frontend: http://localhost:5173
- Stop the stack: `docker compose down`

If a port is already in use, stop the conflicting service before starting Compose.

## CI/CD

The workflow `.github/workflows/ci.yml` runs on PRs and pushes to `main`:

1. Checkout with submodules
2. Lint the **original backend** with its locked uv dependencies
3. Start a temporary PostgreSQL DB and run the upstream migrations and pytest tests
4. Build the original backend and frontend Docker images
5. Publish SHA-tagged backend and frontend images to GHCR only on successful `main` runs

The workflow does **not** deploy to Kubernetes yet. GitOps deployment is the next phase.

See [Phase 1 instructions](docs/phase-1.md) and the [original application README](course-app/README.md).

## Provenance

The application is maintained by DataScientest and retains its upstream MIT license.
This repository demonstrates our DevOps delivery and infrastructure implementation, not authorship of the upstream application.
