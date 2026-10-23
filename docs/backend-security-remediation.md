# Backend security gate remediation — 2026-10-23

## 8. Think About Security (DevSecOps)

The Debian backend at revision `211199d` had **0 CRITICAL / 44 HIGH** package findings and correctly failed the release gate. The rebuilt backend uses **Python 3.12.15 on Alpine 3.24.3**, with the official base pinned by digest, and passes Trivy 0.76.1 with **0 CRITICAL / 0 HIGH** findings. Both OS and Python package results are included. No CVEs are ignored and unfixed findings remain included. This states the HIGH/CRITICAL result at scan time, not immunity from future vulnerabilities.

The build and runtime share the same Alpine base so the virtual environment and native extensions use musl consistently. The upstream FastAPI application, pinned submodule and dependency lock are unchanged. Bash remains installed because the Kubernetes migration init container runs `bash scripts/prestart.sh`. The runtime keeps UID/GID 10001, its original entrypoint and health check.

[Official Python image documentation](https://hub.docker.com/_/python) describes the musl compatibility caveat. Runtime testing below exercises the actual native dependencies instead of assuming Debian-built artifacts work on Alpine.

## 3. Run Tests on the Application

The existing PostgreSQL-backed suite passed: **55 upstream tests and 2 platform tests**. The new `scripts/test-backend-image.py` also tests the exact runtime image against a separate disposable PostgreSQL 16.10 database, sequentially:

- Runs the deployed Bash migration/initialization script as the non-root image user with a read-only root filesystem and all capabilities dropped.
- Starts the default image command and checks health, database readiness and OpenAPI.
- Logs in through bcrypt, authenticates with the returned JWT, and creates, reads and deletes a real database item.
- Checks Prometheus metrics, Docker HEALTHCHECK and UID 10001.
- Removes only its own temporary containers, database, network and generated credential file.

## 5. Automate Deployment (CI/CD Pipeline)

CI now runs the runtime-image check between backend build and the existing strict image scan. Publication still requires all gates and a push to `main`; a successful PR check does not publish images or promote `deploy/dev`. Argo reconciliation, cloud provisioning and production deployment are separate untested outcomes.

**Hosted validation:** [CI run 39928939273](https://github.com/dionis1/liora-devops-platform/actions/runs/39928939273) for commit `34bf33e` completed successfully: backend tests/lint, Terraform/Ansible/Kustomize, exact-image PostgreSQL integration, and backend/frontend image scans. The separate source Security audit also passed. Publication and GitOps promotion were intentionally skipped on the PR event. [Job screenshot](screenshots/08-think-about-security-devsecops/E41.jpg) · [Workflow screenshot](screenshots/05-automate-deployment-ci-cd-pipeline/E42.jpg).

## Concrete evidence

All commands were run sequentially on the local laptop. Source revision before this change: `51921c9`; the fix is recorded by this report's Git commit. The image ID and complete scan output are preserved below. Historical failure evidence remains in the gallery for comparison.

- [Hosted workflow and step records](backend-security-evidence/github-ci-34bf33e.json)
- [Backend scan JSON](backend-security-evidence/trivy-backend.json)
- [Scan command, counts and image identity](backend-security-evidence/summary.txt)
- [Exact runtime-image integration check](backend-security-evidence/runtime-tests.txt)
- [55 upstream and 2 platform tests](backend-security-evidence/backend-tests.txt)
- [Mypy and Ruff](backend-security-evidence/backend-lint.txt)
- [Backend build](backend-security-evidence/build.txt)
- [Source, configuration and secret checks](backend-security-evidence/source-config-secrets.txt)

Reproduce after `bash scripts/prepare-course-app.sh`:

```bash
docker build --pull -f docker/backend.Dockerfile -t liora-backend:ci course-app/backend
python3 scripts/test-backend-image.py liora-backend:ci
trivy image --parallel 1 --severity HIGH,CRITICAL --exit-code 1 liora-backend:ci
bash scripts/test-backend.sh
bash scripts/scan-security.sh
```

Full Kubernetes NetworkPolicy enforcement, Argo sync/rollback and production deployment remain NOT YET TESTED. Older screenshots E09/E28/E29 deliberately retain the previous failing result; use the newer evidence alongside them.

## Later publication and Argo execution

The secure main release db2efa8 was subsequently published and pulled anonymously into real Kubernetes. Argo Synced + Healthy and a controlled configuration rollback passed. The later promotion merge failure and guarded recovery are recorded separately in [the Argo validation report](argocd-validation.md); the historical main run remains failed at promotion.
