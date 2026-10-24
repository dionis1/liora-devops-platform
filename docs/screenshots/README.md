# Visual evidence index

Captures through: 2026-10-24 (Europe/Tirane). Original observation dates and software versions are recorded for every image.

**Actual UI** screenshots show real application, monitoring or GitHub pages. **Archived-output** screenshots show real saved command/API output in a labeled evidence viewer; they are not screenshots taken during the original run. **Configuration/design** views never prove deployment success. All full source artifacts and hashes are preserved.

The exact ten official headings below are the primary organization. [Presentation plans](../presentation-evidence.md) · [Validation checklist](../requirements-validation-checklist.md) · [Machine-readable provenance](manifest.json) · [Offline gallery](../presentation-evidence/index.html) · [Capture protocol](capture-protocol.md)

## 1. Dockerize Your Application

**E01 — FastAPI Swagger documentation** · **PASSED** · `actual-ui`

[Screenshot](01-dockerize-your-application/fastapi-swagger.jpg) · [remediation-report.md](../../docs/presentation-evidence/historical-sources/33c313d09c65cc30731bdbe8d762f47ac5c275440f44af6db0bc07e513957d0f/remediation-report.md)

- Demonstrates: Original patched upstream app; screenshot fixture had no database.
- Supports official requirement(s): 1.
- Captured: 2026-10-23; original observation: 2026-10-23; environment: Local.
- Software: Python 3.12 / FastAPI 0.161.0.
- Command/page: `Open http://127.0.0.1:18000/docs`

**E02 — Original React login page** · **PASSED** · `actual-ui`

[Screenshot](01-dockerize-your-application/react-login.jpg) · [remediation-report.md](../../docs/presentation-evidence/historical-sources/33c313d09c65cc30731bdbe8d762f47ac5c275440f44af6db0bc07e513957d0f/remediation-report.md)

- Demonstrates: Login form rendering only. Authenticated functionality is proved separately by E06–E07.
- Supports official requirement(s): 1.
- Captured: 2026-10-23; original observation: 2026-10-23; environment: Local.
- Software: React 18 / Vite 6.4.4.
- Command/page: `Open http://127.0.0.1:18081/login`

**E06 — Authenticated application dashboard** · **PASSED** · `actual-ui`

[Screenshot](01-dockerize-your-application/authenticated-dashboard.jpg) · [application-live-health.txt](../../docs/presentation-evidence/raw/application-live-health.txt)

- Demonstrates: Actual browser login against an isolated database; no password appears in the screenshot.
- Supports official requirement(s): 1, 3.
- Captured: 2026-10-23; original observation: 2026-10-23; environment: Local.
- Software: Patched upstream app at platform 211199d / PostgreSQL 16.10.
- Command/page: `Sign in to isolated http://127.0.0.1:18081 with temporary local credentials`

**E07 — Browser-created item persists after reload** · **PASSED** · `actual-ui`

[Screenshot](01-dockerize-your-application/item-created-and-persisted.jpg) · [postgres16-browser-record-restore.txt](../../docs/presentation-evidence/raw/postgres16-browser-record-restore.txt)

- Demonstrates: Synthetic item persisted through the API and database; same ID/title restored in E34.
- Supports official requirement(s): 1, 3, 9.
- Captured: 2026-10-23; original observation: 2026-10-23; environment: Local.
- Software: React / FastAPI / PostgreSQL 16.10.
- Command/page: `Items → Add Item → Save → reload`

**E08 — Executed Swagger request returns HTTP 200** · **PASSED** · `actual-ui`

[Screenshot](01-dockerize-your-application/swagger-real-health-200.jpg) · [application-live-health.txt](../../docs/presentation-evidence/raw/application-live-health.txt)

- Demonstrates: Server response 200 and body true, not the schema example. Database readiness separately returned 200.
- Supports official requirement(s): 1.
- Captured: 2026-10-23; original observation: 2026-10-23; environment: Local.
- Software: FastAPI 0.161.0 / Uvicorn.
- Command/page: `Swagger → health-check → Try it out → Execute`

**E13 — Backend image build completed** · **PASSED** · `archived-output`

[Screenshot](01-dockerize-your-application/E13.jpg) · [backend-build.txt](../../docs/remediation-evidence/backend-build.txt)

- Demonstrates: Original build log excerpt; build success does not waive its 44 HIGH OS findings.
- Supports official requirement(s): 1.
- Captured: 2026-10-23; original observation: 2026-10-23; environment: Local.
- Software: Python 3.12 / uv 0.13.1 / Docker 29.1.3.
- Command/page: `docker build -f docker/backend.Dockerfile -t liora-remediation-backend:local course-app/backend`

**E14 — Frontend TypeScript and production bundle completed** · **PASSED** · `archived-output`

[Screenshot](01-dockerize-your-application/E14.jpg) · [frontend-build.txt](../../docs/remediation-evidence/frontend-build.txt)

- Demonstrates: Exact archived build output. Later cached functional fixture reused this application source.
- Supports official requirement(s): 1.
- Captured: 2026-10-23; original observation: 2026-10-23; environment: Local.
- Software: Node 22 / Vite 6.4.4 / Nginx 1.30.
- Command/page: `docker build -f docker/frontend.Dockerfile -t liora-remediation-frontend:local course-app/frontend`

**E15 — Running containers and health checks** · **PASSED** · `archived-output`

[Screenshot](01-dockerize-your-application/E15.jpg) · [docker-running-health.txt](../../docs/presentation-evidence/raw/docker-running-health.txt); [functional-fixture.compose.yml](../../docs/presentation-evidence/raw/functional-fixture.compose.yml)

- Demonstrates: Actual isolated containers with a temporary same-origin Nginx API proxy; no Kubernetes/monitoring was running.
- Supports official requirement(s): 1.
- Captured: 2026-10-23; original observation: 2026-10-23; environment: Local.
- Software: Docker 29.1.3 / PostgreSQL 16.10.
- Command/page: `docker ps; docker inspect (selected health/security fields only)`

**E49 — Public GHCR package exposes the secure release tag** · **PASSED** · `actual-ui`

[Screenshot](01-dockerize-your-application/E49.jpg) · [registry-proof.json](../../docs/argocd-evidence/registry-proof.json)

- Demonstrates: Actual signed-out GitHub package UI: Public badge and current secure image tag. Both backend and frontend anonymous access and running digests are proved separately in E51.
- Supports official requirement(s): 1, 5.
- Captured: 2026-10-23; original observation: 2026-10-23; environment: Local.
- Software: Backend release sha-db2efa81c1037f3b38c4cc615fb7f65d958259c2.
- Command/page: `Open public backend GHCR package page` · [workflow](https://github.com/dionis1/liora-devops-platform/pkgs/container/liora-devops-platform-backend)

**E51 — Anonymous registry reads match the actual running image digests** · **PASSED** · `archived-output`

[Screenshot](01-dockerize-your-application/E51.jpg) · [registry-proof.json](../../docs/argocd-evidence/registry-proof.json); [running-images.json](../../docs/argocd-evidence/running-images.json); [credential-scope.json](../../docs/argocd-evidence/credential-scope.json)

- Demonstrates: Actual HTTP 200 for both released SHA tags; published digests exactly match running pods. Public Git repository visibility and GHCR package visibility were checked independently.
- Supports official requirement(s): 1, 5, 8.
- Captured: 2026-10-23; original observation: 2026-10-23; environment: Local.
- Software: GHCR / k3s 1.35.5-k3s1.
- Command/page: `Anonymous GHCR manifest GET; compare with Kubernetes containerStatuses.imageID`

**E60 — Published image digests match dev and production pods** · **PASSED** · `archived-output`

[Screenshot](01-dockerize-your-application/E60.jpg) · [running-image-proof.txt](../../docs/environment-evidence/running-image-proof.txt); [registry-release.json](../../docs/environment-evidence/registry-release.json); [dev-runtime.json](../../docs/environment-evidence/dev-runtime.json); [prod-runtime.json](../../docs/environment-evidence/prod-runtime.json)

- Demonstrates: Both actual running imageIDs match public registry digests. Prod migration and backend share the immutable reference; no image rebuild for screenshots.
- Supports official requirement(s): 1, 2, 5, 8.
- Captured: 2026-10-24; original observation: 2026-10-24; environment: Disposable local k3d; sequential dev/prod.
- Software: k3s 1.35.5+k3s1 / PostgreSQL 16.10 / secure ef41449 image pair.
- Command/page: `Anonymous GHCR manifest GET; compare published digest to both environments imageIDs`

## 2. Deploy the Application in Multiple Environments (Dev & Prod)

**E19 — Dev and prod separation: static manifests** · **PARTIALLY VALIDATED** · `archived-output`

[Screenshot](02-deploy-the-application-in-multiple-environments-dev-prod/E19.jpg) · [dev-prod-configuration.txt](../../docs/presentation-evidence/raw/dev-prod-configuration.txt)

- Demonstrates: Namespaces, image references, hosts and TLS settings are configuration evidence only. Production was not deployed.
- Supports official requirement(s): 2.
- Captured: 2026-10-23; original observation: 2026-10-23; environment: Local.
- Software: kubectl 1.35.9 / Kustomize 5.7.1.
- Command/page: `kubectl kustomize kubernetes/overlays/dev; kubectl kustomize kubernetes/overlays/prod`

**E53 — Dev browser shows its own persisted record** · **PASSED** · `actual-ui`

[Screenshot](02-deploy-the-application-in-multiple-environments-dev-prod/E53.jpg) · [dev-http.json](../../docs/environment-evidence/dev-http.json); [dev-runtime.json](../../docs/environment-evidence/dev-runtime.json)

- Demonstrates: Actual authenticated dev application, backed by its own Kubernetes PostgreSQL. Temporary same-origin proxy; no public ingress/TLS claim.
- Supports official requirement(s): 2, 3, 4.
- Captured: 2026-10-24; original observation: 2026-10-24; environment: Disposable local k3d; sequential dev/prod.
- Software: k3s 1.35.5+k3s1 / PostgreSQL 16.10 / secure ef41449 image pair.
- Command/page: `Sign in to dev through localhost port-forward proxy; open Items`

**E54 — Current dev Kubernetes workloads and storage are Ready** · **PASSED** · `archived-output`

[Screenshot](02-deploy-the-application-in-multiple-environments-dev-prod/E54.jpg) · [dev-ready.txt](../../docs/environment-evidence/dev-ready.txt)

- Demonstrates: Saved real output, captured before stopping dev web pods. Three ready pods and independent bound PVC; local cluster only.
- Supports official requirement(s): 2, 4.
- Captured: 2026-10-24; original observation: 2026-10-24; environment: Disposable local k3d; sequential dev/prod.
- Software: k3s 1.35.5+k3s1 / PostgreSQL 16.10 / secure ef41449 image pair.
- Command/page: `kubectl -n liora-dev get pods,deploy,sts,svc,pvc,ingress`

**E55 — Dev frontend, API health, readiness and CRUD pass** · **PASSED** · `archived-output`

[Screenshot](02-deploy-the-application-in-multiple-environments-dev-prod/E55.jpg) · [dev-http.json](../../docs/environment-evidence/dev-http.json)

- Demonstrates: Saved actual smoke-test output. Loopback service port-forwards plus a temporary proxy; not public ingress/TLS.
- Supports official requirement(s): 2, 3.
- Captured: 2026-10-24; original observation: 2026-10-24; environment: Disposable local k3d; sequential dev/prod.
- Software: k3s 1.35.5+k3s1 / PostgreSQL 16.10 / secure ef41449 image pair.
- Command/page: `python smoke.py dev; HTTP health, readiness, JWT login, create/read item`

**E56 — Production browser shows a separate persisted record** · **PASSED** · `actual-ui`

[Screenshot](02-deploy-the-application-in-multiple-environments-dev-prod/E56.jpg) · [prod-http.json](../../docs/environment-evidence/prod-http.json); [prod-runtime.json](../../docs/environment-evidence/prod-runtime.json)

- Demonstrates: Actual authenticated production-mode app, independently migrated Kubernetes PostgreSQL and separate Secret. Not cloud/public HTTPS or Argo prod sync.
- Supports official requirement(s): 2, 3, 4.
- Captured: 2026-10-24; original observation: 2026-10-24; environment: Disposable local k3d; sequential dev/prod.
- Software: k3s 1.35.5+k3s1 / PostgreSQL 16.10 / secure ef41449 image pair.
- Command/page: `Sign in to prod through localhost port-forward proxy; open Items`

**E57 — Production Kubernetes workloads and storage are Ready** · **PASSED** · `archived-output`

[Screenshot](02-deploy-the-application-in-multiple-environments-dev-prod/E57.jpg) · [prod-ready.txt](../../docs/environment-evidence/prod-ready.txt)

- Demonstrates: Saved actual production-overlay readiness, three ready pods and a distinct bound PVC. Ingress shown as configuration; public TLS not tested.
- Supports official requirement(s): 2, 4.
- Captured: 2026-10-24; original observation: 2026-10-24; environment: Disposable local k3d; sequential dev/prod.
- Software: k3s 1.35.5+k3s1 / PostgreSQL 16.10 / secure ef41449 image pair.
- Command/page: `Manually apply prod-rendered.yaml; wait for rollouts; kubectl get resources`

**E58 — Production HTTP, database readiness and authenticated CRUD pass** · **PASSED** · `archived-output`

[Screenshot](02-deploy-the-application-in-multiple-environments-dev-prod/E58.jpg) · [prod-http.json](../../docs/environment-evidence/prod-http.json)

- Demonstrates: Saved actual production-mode execution through localhost service port-forwards and proxy. Public DNS, TLS and cloud not exercised.
- Supports official requirement(s): 2, 3.
- Captured: 2026-10-24; original observation: 2026-10-24; environment: Disposable local k3d; sequential dev/prod.
- Software: k3s 1.35.5+k3s1 / PostgreSQL 16.10 / secure ef41449 image pair.
- Command/page: `python smoke.py prod; HTTP health, readiness, JWT login, create/read item`

**E59 — Cross-environment isolation is verified in both directions** · **PASSED** · `archived-output`

[Screenshot](02-deploy-the-application-in-multiple-environments-dev-prod/E59.jpg) · [isolation-summary.txt](../../docs/environment-evidence/isolation-summary.txt); [dev-isolation.json](../../docs/environment-evidence/dev-isolation.json); [prod-isolation.json](../../docs/environment-evidence/prod-isolation.json); [dev-recheck.json](../../docs/environment-evidence/dev-recheck.json)

- Demonstrates: Own DB TCP succeeds, cross-namespace DB connection rejected, wrong-environment credentials HTTP 400 and records HTTP 404. Both target DBs live. No node-level failure separation.
- Supports official requirement(s): 2, 4, 8.
- Captured: 2026-10-24; original observation: 2026-10-24; environment: Disposable local k3d; sequential dev/prod.
- Software: k3s 1.35.5+k3s1 / PostgreSQL 16.10 / secure ef41449 image pair.
- Command/page: `python isolate.py prod; stop prod web; restore dev; python isolate.py dev`

**E61 — Runtime configuration, Secret objects and storage are separated** · **PASSED** · `archived-output`

[Screenshot](02-deploy-the-application-in-multiple-environments-dev-prod/E61.jpg) · [environment-separation.txt](../../docs/environment-evidence/environment-separation.txt); [dev-runtime.json](../../docs/environment-evidence/dev-runtime.json); [prod-runtime.json](../../docs/environment-evidence/prod-runtime.json)

- Demonstrates: Actual namespace-local configuration/Secret/PVC metadata; no secret values. Full web stacks tested sequentially, not concurrently.
- Supports official requirement(s): 2, 8.
- Captured: 2026-10-24; original observation: 2026-10-24; environment: Disposable local k3d; sequential dev/prod.
- Software: k3s 1.35.5+k3s1 / PostgreSQL 16.10 / secure ef41449 image pair.
- Command/page: `Inspect ConfigMaps, Secret UIDs/keys and PVC volume names; compare values only in memory`

**E62 — Both overlays render and production approval policy is preserved** · **PASSED** · `archived-output`

[Screenshot](02-deploy-the-application-in-multiple-environments-dev-prod/E62.jpg) · [render-summary.txt](../../docs/environment-evidence/render-summary.txt); [manifest-validation.json](../../docs/environment-evidence/manifest-validation.json); [overlay-changes.patch](../../docs/environment-evidence/overlay-changes.patch)

- Demonstrates: Static evidence only: zero rendered bootstrap references, migration image matches backend, dev auto-sync and prod manual main policy unchanged. Runtime evidence separate.
- Supports official requirement(s): 2, 4, 5.
- Captured: 2026-10-24; original observation: 2026-10-24; environment: Disposable local k3d; sequential dev/prod.
- Software: k3s 1.35.5+k3s1 / PostgreSQL 16.10 / secure ef41449 image pair.
- Command/page: `kubectl kustomize both overlays; verify image replacement and GitOps policies`

## 3. Run Tests on the Application

**E16 — 55 upstream tests passed** · **PASSED** · `archived-output`

[Screenshot](03-run-tests-on-the-application/E16.jpg) · [backend-tests.txt](../../docs/remediation-evidence/backend-tests.txt)

- Demonstrates: Original captured test counts and result; passlib deprecation warning remains.
- Supports official requirement(s): 3.
- Captured: 2026-10-23; original observation: 2026-10-23; environment: Local.
- Software: Python 3.12.3 / pytest 7.4.4 / PostgreSQL 16.10.
- Command/page: `uv run --frozen bash scripts/tests-start.sh`

**E17 — Platform metrics and readiness tests passed** · **PASSED** · `archived-output`

[Screenshot](03-run-tests-on-the-application/E17.jpg) · [metrics-tests.txt](../../docs/remediation-evidence/metrics-tests.txt)

- Demonstrates: Request/status/duration metrics and safe database-unavailable 503 response.
- Supports official requirement(s): 3.
- Captured: 2026-10-23; original observation: 2026-10-23; environment: Local.
- Software: Python 3.12 / pytest 7.4.4.
- Command/page: `python -m pytest tests/test_platform_metrics.py -q`

**E18 — Mypy and Ruff passed** · **PASSED** · `archived-output`

[Screenshot](03-run-tests-on-the-application/E18.jpg) · [backend-lint.txt](../../docs/remediation-evidence/backend-lint.txt)

- Demonstrates: Actual archived lint output for 39 source files.
- Supports official requirement(s): 3.
- Captured: 2026-10-23; original observation: 2026-10-23; environment: Local.
- Software: Mypy / Ruff 0.17.2.
- Command/page: `uv run --frozen bash scripts/lint.sh`

## 4. Container Orchestration with Kubernetes

**E20 — Historical dev pods and Services READY** · **PASSED** · `archived-output`

[Screenshot](04-container-orchestration-with-kubernetes/E20.jpg) · [kubernetes-live.log](../../docs/local-validation-evidence/kubernetes-live.log)

- Demonstrates: Archived actual first-pass local cluster; cluster deleted. Final second-pass hardening was not deployed.
- Supports official requirement(s): 4.
- Captured: 2026-10-23; original observation: 2026-10-22; environment: Local.
- Software: k3d 5.9.0 / default k3s 1.35.5-k3s1 / PostgreSQL 16.10.
- Command/page: `kubectl -n liora-dev get pods,services,pvc -o wide`

**E21 — Historical PVC and Kubernetes HTTP access** · **PASSED** · `archived-output`

[Screenshot](04-container-orchestration-with-kubernetes/E21.jpg) · [kubernetes-live.log](../../docs/local-validation-evidence/kubernetes-live.log)

- Demonstrates: Actual first-pass bound 8 GiB PVC and local backend/frontend/Traefik checks. Not cloud/public HTTPS.
- Supports official requirement(s): 4.
- Captured: 2026-10-23; original observation: 2026-10-22; environment: Local.
- Software: k3d 5.9.0 / PostgreSQL 16.10 / Traefik.
- Command/page: `kubectl get pvc; loopback port-forward HTTP requests; Traefik routing smoke`

**E37 — Historical ConfigMap, Ingress and rollout results** · **PASSED** · `archived-output`

[Screenshot](04-container-orchestration-with-kubernetes/E37.jpg) · [kubernetes-live.log](../../docs/local-validation-evidence/kubernetes-live.log)

- Demonstrates: Actual first-pass resource creation and rollout output. New security/metrics manifests were not deployed.
- Supports official requirement(s): 4.
- Captured: 2026-10-23; original observation: 2026-10-22; environment: Local.
- Software: k3d 5.9.0 / original first-pass images.
- Command/page: `kubectl apply local-dev.yaml; rollout status postgres/backend/frontend`

**E45 — Current hardened dev workloads, node and PVC are ready** · **PASSED** · `archived-output`

[Screenshot](04-container-orchestration-with-kubernetes/E45.jpg) · [ready-summary.txt](../../docs/argocd-evidence/ready-summary.txt)

- Demonstrates: Real local output: node Ready, all three app pods 1/1, deployments/statefulset ready, 8 GiB PVC Bound and Traefik Ingress. No cloud/production claim.
- Supports official requirement(s): 2, 4, 5.
- Captured: 2026-10-23; original observation: 2026-10-23; environment: Local.
- Software: k3d 5.9.0 / k3s 1.35.5-k3s1 / PostgreSQL 16.10.
- Command/page: `kubectl get nodes; kubectl -n liora-dev get pods,deploy,sts,pvc,ingress`

## 5. Automate Deployment (CI/CD Pipeline)

**E09 — Historical Debian CI blocks publication** · **FAILED** · `actual-ui`

[Screenshot](05-automate-deployment-ci-cd-pipeline/github-current-security-gate.jpg) · [github-ci-211199d.json](../../docs/presentation-evidence/raw/github-ci-211199d.json)

- Demonstrates: Tests/lint/platform checks passed; backend image scan failed; publication/promotion skipped. PR publication is also restricted to main push events.
- Supports official requirement(s): 5.
- Captured: 2026-10-23; original observation: 2026-10-23; environment: GitHub Actions.
- Software: Commit 211199d.
- Command/page: `Open current workflow run` · [workflow](https://github.com/dionis1/liora-devops-platform/actions/runs/39920280796)

**E10 — Historical successful GHCR publication and dev promotion** · **PASSED** · `actual-ui`

[Screenshot](05-automate-deployment-ci-cd-pipeline/github-historical-publish-promote.jpg) · [github-historical-ci-main.json](../../docs/presentation-evidence/raw/github-historical-ci-main.json)

- Demonstrates: Historical publication/promotion only; not a release of 211199d and not Argo deployment proof.
- Supports official requirement(s): 1, 5.
- Captured: 2026-10-23; original observation: 2026-10-22; environment: GitHub Actions.
- Software: Commit 3ca9925; older pipeline.
- Command/page: `Open historical main workflow run` · [workflow](https://github.com/dionis1/liora-devops-platform/actions/runs/39802778100)

**E22 — Argo CD ran, but private repository comparison failed** · **FAILED** · `archived-output`

[Screenshot](05-automate-deployment-ci-cd-pipeline/E22.jpg) · [argocd-live.log](../../docs/local-validation-evidence/argocd-live.log)

- Demonstrates: Health is not synchronization. Historical private-repo ComparisonError. Repository became public on 2026-10-23; new public reconciliation still not tested.
- Supports official requirement(s): 5.
- Captured: 2026-10-23; original observation: 2026-10-22; environment: Local.
- Software: Argo CD 3.5.5 / local k3d.
- Command/page: `Argo CD health; kubectl get applications`

**E23 — Production manual sync configuration** · **PARTIALLY VALIDATED** · `configuration`

[Screenshot](05-automate-deployment-ci-cd-pipeline/E23.jpg) · [applications.yaml](../../gitops/applications.yaml)

- Demonstrates: Design/static proof only. No successful production sync or rollback is claimed.
- Supports official requirement(s): 5.
- Captured: 2026-10-23; original observation: 2026-10-23; environment: Local.
- Software: Application manifests at 211199d.
- Command/page: `Review gitops/applications.yaml; no automated production policy`

**E38 — Historical Argo components ready; sync still unproven** · **PARTIALLY VALIDATED** · `archived-output`

[Screenshot](05-automate-deployment-ci-cd-pipeline/E38.jpg) · [argocd-live.log](../../docs/local-validation-evidence/argocd-live.log)

- Demonstrates: Actual running controllers/repository/server components. GitHub comparison failed afterward (E22); this is not Synced/Healthy application proof.
- Supports official requirement(s): 5.
- Captured: 2026-10-23; original observation: 2026-10-22; environment: Local.
- Software: Argo CD 3.5.5 / local k3d.
- Command/page: `kubectl -n argocd get pods,services; Argo health check`

**E42 — Complete Alpine fix CI workflow succeeds** · **PASSED** · `actual-ui`

[Screenshot](05-automate-deployment-ci-cd-pipeline/E42.jpg) · [github-ci-34bf33e.json](../../docs/backend-security-evidence/github-ci-34bf33e.json)

- Demonstrates: Real GitHub summary: tests, lint, platform validation and build/scan passed. Publishing/promotion intentionally skip because this is a PR, not a push to main.
- Supports official requirement(s): 1, 3, 5, 8.
- Captured: 2026-10-23; original observation: 2026-10-23; environment: GitHub Actions.
- Software: Commit 34bf33e / workflow run 39928939273.
- Command/page: `Open successful CI run for PR 16 / commit 34bf33e` · [workflow](https://github.com/dionis1/liora-devops-platform/actions/runs/39928939273)

**E43 — Argo development Application is Synced and Healthy** · **PASSED** · `actual-ui`

[Screenshot](05-automate-deployment-ci-cd-pipeline/E43.jpg) · [dev-sync.json](../../docs/argocd-evidence/dev-sync.json)

- Demonstrates: Actual disposable local Argo UI, public GitHub deploy/dev at 1b0ffd5, real anonymous GHCR pulls; not a production/cloud deployment.
- Supports official requirement(s): 1, 4, 5.
- Captured: 2026-10-23; original observation: 2026-10-23; environment: Local.
- Software: Argo CD 3.5.5 / chart 10.10.5 / k3s 1.35.5-k3s1.
- Command/page: `Apply gitops/applications.yaml dev Application; wait for exact promoted revision`

**E44 — Canonical dev branch restored after successful rollback test** · **PASSED** · `actual-ui`

[Screenshot](05-automate-deployment-ci-cd-pipeline/E44.jpg) · [final-dev-sync.json](../../docs/argocd-evidence/final-dev-sync.json)

- Demonstrates: Actual final dev state after the isolated Git-revert drill. Auto-sync enabled; rollback test did not modify deploy/dev. Cluster removed after evidence capture.
- Supports official requirement(s): 4, 5, 9.
- Captured: 2026-10-23; original observation: 2026-10-23; environment: Local.
- Software: Argo CD 3.5.5 / dev revision 1b0ffd5.
- Command/page: `Restore targetRevision deploy/dev; check exact 1b0ffd5 Synced/Healthy/Succeeded`

**E46 — Argo rolls out the controlled changed Git revision** · **PASSED** · `actual-ui`

[Screenshot](05-automate-deployment-ci-cd-pipeline/E46.jpg) · [rollback-changed.json](../../docs/argocd-evidence/rollback-changed.json)

- Demonstrates: Actual changed backend template reached Synced/Healthy with a new ReplicaSet. Secure image tag unchanged; same database record remained accessible.
- Supports official requirement(s): 4, 5, 9.
- Captured: 2026-10-23; original observation: 2026-10-23; environment: Local.
- Software: Argo CD 3.5.5 / changed revision 0c279d4.
- Command/page: `Push 0c279d4 to isolated rollback branch; hard refresh; auto-sync and readiness checks`

**E50 — Secure image publication succeeds; promotion initially fails** · **PASSED** · `actual-ui`

[Screenshot](05-automate-deployment-ci-cd-pipeline/E50.jpg) · [release-jobs.json](../../docs/argocd-evidence/release-jobs.json)

- Demonstrates: Publication job PASSED. Overall run FAILED on the later merge conflict; reviewed script recovered promotion separately. This screenshot does not claim the complete main workflow passed.
- Supports official requirement(s): 1, 5.
- Captured: 2026-10-23; original observation: 2026-10-23; environment: GitHub Actions.
- Software: Main db2efa8 / workflow run 39931016209.
- Command/page: `Open successful Publish only scanned images job` · [workflow](https://github.com/dionis1/liora-devops-platform/actions/runs/39931016209/job/120340274170)

**E52 — Latest main tests, scans, publication and dev promotion all pass** · **PASSED** · `actual-ui`

[Screenshot](05-automate-deployment-ci-cd-pipeline/E52.jpg) · [release-jobs.json](../../docs/environment-evidence/release-jobs.json)

- Demonstrates: Actual successful hosted main run at ef41449. Not the earlier failed db2efa8 run; does not prove prod Argo synchronization.
- Supports official requirement(s): 1, 3, 5, 6, 8.
- Captured: 2026-10-24; original observation: 2026-10-23; environment: GitHub Actions.
- Software: Main ef41449 / release sha-ef414490d99151a3640cea6dac56589531816694.
- Command/page: `Open main workflow 39939061134` · [workflow](https://github.com/dionis1/liora-devops-platform/actions/runs/39939061134)

## 6. Create IaC (Infrastructure as Code) Templates

**E11 — Current Terraform, Ansible and Kustomize workflow passes** · **PASSED** · `actual-ui`

[Screenshot](06-create-iac-infrastructure-as-code-templates/github-platform-validation-passed.jpg) · [github-platform-211199d.json](../../docs/presentation-evidence/raw/github-platform-211199d.json)

- Demonstrates: Static checks only; no Terraform plan/apply or k3s provisioning.
- Supports official requirement(s): 2, 4, 6.
- Captured: 2026-10-23; original observation: 2026-10-23; environment: GitHub Actions.
- Software: Commit 211199d.
- Command/page: `Open platform validation workflow` · [workflow](https://github.com/dionis1/liora-devops-platform/actions/runs/39920280791)

**E24 — Terraform formatting and validation passed** · **PASSED** · `archived-output`

[Screenshot](06-create-iac-infrastructure-as-code-templates/E24.jpg) · [terraform-validation.txt](../../docs/presentation-evidence/raw/terraform-validation.txt)

- Demonstrates: Actual fresh command output; no plan/apply or cloud recreation.
- Supports official requirement(s): 6.
- Captured: 2026-10-23; original observation: 2026-10-23; environment: Local.
- Software: Terraform 1.16.6.
- Command/page: `terraform fmt -check -recursive; terraform validate`

**E25 — Three Ansible syntax checks passed** · **PASSED** · `archived-output`

[Screenshot](06-create-iac-infrastructure-as-code-templates/E25.jpg) · [ansible-validation.txt](../../docs/presentation-evidence/raw/ansible-validation.txt)

- Demonstrates: Actual fresh syntax output. No remote installation or cloud host validation.
- Supports official requirement(s): 6.
- Captured: 2026-10-23; original observation: 2026-10-23; environment: Local.
- Software: Ansible core 2.16.3 / Python 3.12.3.
- Command/page: `ansible-playbook --syntax-check prepare.yml / k3s.yml / kubeconfig.yml`

## 7. Monitor the Application

**E03 — All three Prometheus targets UP** · **PASSED** · `actual-ui`

[Screenshot](07-monitor-the-application/prometheus-targets-up.jpg) · [monitoring-targets.json](../../docs/remediation-evidence/monitoring-targets.json)

- Demonstrates: Isolated Docker targets; not proof of ServiceMonitor discovery in Kubernetes.
- Supports official requirement(s): 7.
- Captured: 2026-10-23; original observation: 2026-10-23; environment: Local.
- Software: Prometheus 3.15.0 / Grafana 13.2.4.
- Command/page: `Open http://127.0.0.1:18084/targets`

**E04 — Real request counts, error counts and latency** · **PASSED** · `actual-ui`

[Screenshot](07-monitor-the-application/grafana-request-latency-errors.jpg) · [fastapi.json](../../monitoring/dashboards/fastapi.json)

- Demonstrates: Synthetic local health requests and deliberate 404s; no production traffic.
- Supports official requirement(s): 7.
- Captured: 2026-10-23; original observation: 2026-10-23; environment: Local.
- Software: Grafana 13.2.4.
- Command/page: `Open http://127.0.0.1:18083/d/liora-fastapi`

**E05 — Unavailable alert FIRING after one minute** · **PASSED** · `actual-ui`

[Screenshot](07-monitor-the-application/application-alert-firing.jpg) · [alert-firing.json](../../docs/remediation-evidence/alert-firing.json)

- Demonstrates: Disposable backend deliberately stopped. Receiver notification delivery not tested.
- Supports official requirement(s): 7.
- Captured: 2026-10-23; original observation: 2026-10-23; environment: Local.
- Software: Prometheus 3.15.0.
- Command/page: `Open http://127.0.0.1:18084/alerts`

**E26 — Application alert cleared after recovery** · **PASSED** · `archived-output`

[Screenshot](07-monitor-the-application/E26.jpg) · [alert-resolved.json](../../docs/remediation-evidence/alert-resolved.json)

- Demonstrates: Actual API record with alerts empty after the firing scenario; notification delivery not tested.
- Supports official requirement(s): 7.
- Captured: 2026-10-23; original observation: 2026-10-23; environment: Local.
- Software: Prometheus 3.15.0.
- Command/page: `GET http://127.0.0.1:18084/api/v1/alerts after backend restart`

**E27 — ServiceMonitor implemented: runtime discovery pending** · **PARTIALLY VALIDATED** · `configuration`

[Screenshot](07-monitor-the-application/E27.jpg) · [application-observability.yaml](../../monitoring/application-observability.yaml)

- Demonstrates: Rendered configuration only. The new ServiceMonitor was not live-tested against the hardened Kubernetes workloads.
- Supports official requirement(s): 7.
- Captured: 2026-10-23; original observation: 2026-10-23; environment: Local.
- Software: monitoring.coreos.com/v1 / chart 92.11.0.
- Command/page: `kubectl kustomize monitoring`

## 8. Think About Security (DevSecOps)

**E12 — Current source security workflow passes** · **PASSED** · `actual-ui`

[Screenshot](08-think-about-security-devsecops/github-source-security-passed.jpg) · [github-source-security-211199d.json](../../docs/presentation-evidence/raw/github-source-security-211199d.json)

- Demonstrates: Patched dependency/configuration/secret scan; not a passing backend-image scan.
- Supports official requirement(s): 8.
- Captured: 2026-10-23; original observation: 2026-10-23; environment: GitHub Actions.
- Software: Trivy 0.76.1 / commit 211199d.
- Command/page: `Open source security workflow` · [workflow](https://github.com/dionis1/liora-devops-platform/actions/runs/39920280780)

**E28 — Security before and after remediation** · **FAILED** · `archived-output`

[Screenshot](08-think-about-security-devsecops/E28.jpg) · [security-findings.json](../../docs/local-validation-evidence/security-findings.json); [security-summary.json](../../docs/remediation-evidence/security-summary.json)

- Demonstrates: Counts derived from archived reports, not a new scan. Different frontend stages are labeled explicitly; no claim that all findings are fixed.
- Supports official requirement(s): 8.
- Captured: 2026-10-23; original observation: 2026-10-23; environment: Local.
- Software: Trivy 0.76.1.
- Command/page: `Compare original Trivy findings with final remediation scan counts`

**E29 — Historical Debian security gate fails closed** · **FAILED** · `archived-output`

[Screenshot](08-think-about-security-devsecops/E29.jpg) · [github-backend-scan-failed.txt](../../docs/presentation-evidence/raw/github-backend-scan-failed.txt)

- Demonstrates: Actual failed job output; 44 HIGH and 0 CRITICAL. Publication remains blocked.
- Supports official requirement(s): 8.
- Captured: 2026-10-23; original observation: 2026-10-23; environment: GitHub Actions.
- Software: Trivy 0.76.1 / 211199d.
- Command/page: `trivy image --parallel 1 --severity HIGH,CRITICAL --exit-code 1 liora-backend:ci` · [workflow](https://github.com/dionis1/liora-devops-platform/actions/runs/39920280796/job/120303913550)

**E30 — Container security controls configured** · **PARTIALLY VALIDATED** · `configuration`

[Screenshot](08-think-about-security-devsecops/E30.jpg) · [container-security-context.txt](../../docs/presentation-evidence/raw/container-security-context.txt)

- Demonstrates: Static configuration. Fresh Docker fixture separately verified read-only/non-root operation; final Kubernetes deployment untested.
- Supports official requirement(s): 8.
- Captured: 2026-10-23; original observation: 2026-10-23; environment: Local.
- Software: Kubernetes manifests at 211199d.
- Command/page: `Review rendered workload security contexts`

**E31 — Default-deny policy and explicit database traffic** · **PARTIALLY VALIDATED** · `configuration`

[Screenshot](08-think-about-security-devsecops/E31.jpg) · [networkpolicy.yaml](../../kubernetes/base/networkpolicy.yaml)

- Demonstrates: Configuration only. Policy enforcement on a live cluster remains NOT YET TESTED.
- Supports official requirement(s): 8.
- Captured: 2026-10-23; original observation: 2026-10-23; environment: Local.
- Software: networking.k8s.io/v1.
- Command/page: `Review NetworkPolicy resources; kubectl kustomize overlays`

**E32 — Temporary credential access removed** · **PASSED** · `archived-output`

[Screenshot](08-think-about-security-devsecops/E32.jpg) · [key-cleanup.json](../../docs/remediation-evidence/key-cleanup.json)

- Demonstrates: Cleanup evidence only. A read-only repository deploy key was not verified or installed; no key material is shown.
- Supports official requirement(s): 8.
- Captured: 2026-10-23; original observation: 2026-10-23; environment: Local.
- Software: GitHub API / 2026-10-23.
- Command/page: `Exact public-key match; approved removal; API absence verified`

**E39 — Alpine backend security gate passes** · **PASSED** · `archived-output`

[Screenshot](08-think-about-security-devsecops/E39.jpg) · [summary.txt](../../docs/backend-security-evidence/summary.txt); [trivy-backend.json](../../docs/backend-security-evidence/trivy-backend.json)

- Demonstrates: Actual new local scan: 0 HIGH/CRITICAL in OS and Python packages, including unfixed findings. Not proof of hosted publication or GitOps deployment.
- Supports official requirement(s): 1, 5, 8.
- Captured: 2026-10-23; original observation: 2026-10-23; environment: Local.
- Software: Trivy 0.76.1 / Python 3.12.15 / Alpine 3.24.3.
- Command/page: `trivy image --parallel 1 --severity HIGH,CRITICAL --exit-code 1 liora-backend:security-fix`

**E40 — Exact Alpine image passes PostgreSQL integration checks** · **PASSED** · `archived-output`

[Screenshot](08-think-about-security-devsecops/E40.jpg) · [runtime-tests.txt](../../docs/backend-security-evidence/runtime-tests.txt)

- Demonstrates: Actual runtime-image test: migrations, login/JWT, database CRUD, health, readiness and metrics under non-root/read-only restrictions. Temporary resources cleaned up.
- Supports official requirement(s): 1, 3, 5, 8.
- Captured: 2026-10-23; original observation: 2026-10-23; environment: Local.
- Software: Python 3.12.15 / Alpine 3.24.3 / PostgreSQL 16.10.
- Command/page: `python3 scripts/test-backend-image.py liora-backend:security-fix`

**E41 — Hosted backend image security gate passes** · **PASSED** · `actual-ui`

[Screenshot](08-think-about-security-devsecops/E41.jpg) · [github-ci-34bf33e.json](../../docs/backend-security-evidence/github-ci-34bf33e.json)

- Demonstrates: Real GitHub job UI: image PostgreSQL integration and both strict image scans passed. Publication artifacts are skipped on PR events by policy.
- Supports official requirement(s): 1, 3, 5, 8.
- Captured: 2026-10-23; original observation: 2026-10-23; environment: GitHub Actions.
- Software: Trivy 0.76.1 / commit 34bf33e.
- Command/page: `Open successful build/scan job for 34bf33e` · [workflow](https://github.com/dionis1/liora-devops-platform/actions/runs/39928939273/job/120332436123)

## 9. Think About Disaster Recovery

**E33 — Actual backup creation and mode 0600** · **PASSED** · `archived-output`

[Screenshot](09-think-about-disaster-recovery/E33.jpg) · [postgres16-browser-record-restore.txt](../../docs/presentation-evidence/raw/postgres16-browser-record-restore.txt)

- Demonstrates: Actual script via explicit kubectl-to-Docker adapter; no Kubernetes/cloud restore claim. Binary dump excluded from Git.
- Supports official requirement(s): 9.
- Captured: 2026-10-23; original observation: 2026-10-23; environment: Local.
- Software: PostgreSQL 16.10 / Docker isolated fixture.
- Command/page: `bash scripts/backup-postgres.sh liora-dev; stat BACKUP`

**E34 — Restored record matches the browser-created item** · **PASSED** · `archived-output`

[Screenshot](09-think-about-disaster-recovery/E34.jpg) · [postgres16-browser-record-restore.txt](../../docs/presentation-evidence/raw/postgres16-browser-record-restore.txt)

- Demonstrates: Actual source/restored rows. Same synthetic UUID/title as E07. Existing user databases were untouched.
- Supports official requirement(s): 9.
- Captured: 2026-10-23; original observation: 2026-10-23; environment: Local.
- Software: PostgreSQL 16.10.
- Command/page: `pg_restore into NEW defense_restore; SELECT id,title FROM item`

**E35 — Failed backups leave no completed corrupt archive** · **PASSED** · `archived-output`

[Screenshot](09-think-about-disaster-recovery/E35.jpg) · [disaster-recovery.txt](../../docs/remediation-evidence/disaster-recovery.txt)

- Demonstrates: Actual prior test output. Expected command failure is a passing negative-control assertion, not a real backup success.
- Supports official requirement(s): 9.
- Captured: 2026-10-23; original observation: 2026-10-23; environment: Local.
- Software: PostgreSQL 16.10 / negative-control test.
- Command/page: `Deliberately fail pg_dump; reject unrelated namespace`

**E47 — Git revert restores a healthy backend deployment** · **PASSED** · `actual-ui`

[Screenshot](09-think-about-disaster-recovery/E47.jpg) · [rollback-reverted.json](../../docs/argocd-evidence/rollback-reverted.json); [rollback-proof.txt](../../docs/argocd-evidence/rollback-proof.txt)

- Demonstrates: Actual configuration rollback on isolated GitHub branch: original template hash and ReplicaSet restored; record unchanged. Not an image-version or schema downgrade.
- Supports official requirement(s): 4, 5, 9.
- Captured: 2026-10-23; original observation: 2026-10-23; environment: Local.
- Software: Argo CD 3.5.5 / revert bf1a495 / PostgreSQL 16.10.
- Command/page: `git revert 0c279d4; push bf1a495; Argo auto-sync; compare template hashes`

**E48 — Argo history records changed revision and Git revert** · **PASSED** · `actual-ui`

[Screenshot](09-think-about-disaster-recovery/E48.jpg) · [rollback-reverted.json](../../docs/argocd-evidence/rollback-reverted.json)

- Demonstrates: Actual auto-sync history, with revert and prior change visible. Full baseline/change/revert history is preserved in JSON; native rollback button was not used.
- Supports official requirement(s): 5, 9.
- Captured: 2026-10-23; original observation: 2026-10-23; environment: Local.
- Software: Argo CD 3.5.5 / baseline 1107506, change 0c279d4, revert bf1a495.
- Command/page: `Argo HISTORY AND ROLLBACK after successful Git revert`

## 10. Documentation

**E36 — Architecture and engineering boundaries** · **PASSED** · `design`

[Screenshot](10-documentation/E36.jpg) · [architecture.md](../../docs/presentation-evidence/historical-sources/e5220972cc7148594b5922e7caf548012419575312b3c34cdc8d97247f789f94/architecture.md)

- Demonstrates: Design diagram, not proof of a Hetzner deployment. Future cloud and manual production steps are labeled.
- Supports official requirement(s): 10.
- Captured: 2026-10-23; original observation: 2026-10-23; environment: Local.
- Software: Platform architecture at 211199d.
- Command/page: `Review architecture.md and the official requirement checklist`

## Missing execution or unavailable screenshots

[Detailed gaps and capture blockers](../presentation-evidence/missing-evidence.md). Every requirement has concrete evidence; several still lack successful end-to-end deployment proof.
