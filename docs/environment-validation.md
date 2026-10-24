# Dev and prod runtime validation — 2026-10-24

**Requirement 2 — Deploy the Application in Multiple Environments (Dev & Prod): PASSED for sequential local deployment.** Both actual Kubernetes overlays were deployed and exercised, with independent credentials, configuration and PostgreSQL storage. This is not proof of public HTTPS, cloud production readiness, concurrent full-stack operation or a production Argo synchronization.

## Release selection and implementation

The approved image pair comes from main `ef414490d99151a3640cea6dac56589531816694`. [Workflow 39939061134](https://github.com/dionis1/liora-devops-platform/actions/runs/39939061134) passed tests, lint, platform validation, strict security scans, image publication and dev promotion. Anonymous GHCR manifest requests returned HTTP 200; manifest SHA-256 values matched the registry response headers. Running image IDs in **both** namespaces matched those digests.

| Component | Immutable production reference |
| --- | --- |
| Backend and migration init-container | `ghcr.io/dionis1/liora-devops-platform-backend@sha256:1b5a8045185f9caae6d293c5d8d6398d4a1bbc6b8e23979b26cf871fac56738b` |
| Frontend | `ghcr.io/dionis1/liora-devops-platform-frontend@sha256:eeebf408bc90040dbf581d98d5092ecbe8d751d2398b82e8471e439ad406310e` |

Production now uses Kustomize `digest` entries instead of `sha-bootstrap`. Dev uses `sha-ef414490d99151a3640cea6dac56589531816694`, matching the latest verified automatic promotion. The PostgreSQL manifest remains `postgres:16.10`. Both environment renders, including the migration init-container, contain no unresolved bootstrap image. [Registry evidence](environment-evidence/registry-release.json) · [actual image identity proof](environment-evidence/running-image-proof.txt) · [exact overlay changes](environment-evidence/overlay-changes.patch).

`gitops/applications.yaml` is unchanged: dev follows `deploy/dev` with auto-sync/prune/self-heal; prod follows `main` with **no automated sync policy**. These local tests used explicit manual `kubectl apply`, not an Argo prod synchronization. The new production pins must reach main through normal review before canonical `liora-prod` can use them. PR #18's guarded promotion helper has passed PR checks but still needs a hosted main execution after merge; the successful ef41449 promotion used the existing main workflow.

## Actual commands and results

The installed k3d 5.9.0 created `liora-env-20261024` with one k3s 1.35.5+k3s1 server, a 2048 MiB Docker memory cap, no agents/load-balancer container, and Kubernetes API bound to `127.0.0.1:16554`. No Argo/monitoring stack or builds ran alongside it. Unrelated `infra-agent-1`, `infra-docker-1` and `infra-jenkins-1` were preserved.

```bash
k3d cluster create liora-env-20261024 \
  --image rancher/k3s:v1.35.5-k3s1 --servers 1 --agents 0 \
  --servers-memory 2048m --no-lb --api-port 127.0.0.1:16554 \
  --k3s-arg '--disable=metrics-server@server:0' \
  --kubeconfig-update-default=false --kubeconfig-switch-context=false \
  --wait --timeout 180s
k3d kubeconfig get liora-env-20261024 > /tmp/liora-env-20261024/kubeconfig
chmod 600 /tmp/liora-env-20261024/kubeconfig
export KUBECONFIG=/tmp/liora-env-20261024/kubeconfig
kubectl kustomize kubernetes/overlays/dev > /tmp/dev.yaml
kubectl kustomize kubernetes/overlays/prod > /tmp/prod.yaml
```

Both renders passed checks for namespaces, Services, ConfigMaps/Secret references, Deployments, StatefulSet/PVC, Ingress, five NetworkPolicies per namespace, resource/security settings, and migration-image replacement. [Static acceptance result](environment-evidence/manifest-validation.json). Existing security gates were retained. CI now also rejects production bootstrap tags, requires three immutable application image references (including migration), and checks that migration and backend match. The guard was executed locally against the real render and passed.

Separate mode-0600 temporary files supplied random database passwords, signing keys, admin emails and admin passwords. No credential values were committed. Namespace manifests were applied first, then each namespace received its own `course-app-secrets`. The normal reusable secret-creation procedure is in [deployment.md](deployment.md); tests used equivalent explicit-kubeconfig commands with `/tmp/liora-env-20261024/dev.env` and `prod.env`.

For **each** environment, sequentially:

```bash
# Dev first; prod only after scaling dev backend/frontend to zero.
kubectl apply -k kubernetes/overlays/dev
kubectl -n liora-dev rollout status statefulset/postgres --timeout=240s
kubectl -n liora-dev rollout status deployment/backend --timeout=240s
kubectl -n liora-dev rollout status deployment/frontend --timeout=180s
# After dev capture:
kubectl -n liora-dev scale deployment/backend deployment/frontend --replicas=0
kubectl apply -k kubernetes/overlays/prod
kubectl -n liora-prod rollout status statefulset/postgres --timeout=180s
kubectl -n liora-prod rollout status deployment/backend --timeout=180s
kubectl -n liora-prod rollout status deployment/frontend --timeout=180s
```

The executed applies used the saved rendered YAML rather than re-rendering during apply; they have identical recorded content. All rollout commands succeeded. Each environment had backend/frontend/PostgreSQL pods **1/1 Ready**, zero current container restarts, ready Deployments/StatefulSet, three Services and its own Bound 8 GiB PVC. [Dev readiness](environment-evidence/dev-ready.txt) · [Prod readiness](environment-evidence/prod-ready.txt) · [runtime snapshots](environment-evidence/prod-runtime.json).

For HTTP testing, the active environment's backend Service was forwarded to `127.0.0.1:18080`, frontend Service to `127.0.0.1:18082`. A temporary [same-origin HTTP proxy](environment-evidence/probes/proxy.py) listened only on `127.0.0.1:18081`; `/api`, `/readyz` and `/metrics` went to backend, other paths to frontend. This exercises service port-forward access; it **does not test the production Ingress/TLS path**.

```bash
# Run these in separate terminals for the active namespace; stop before switching.
kubectl -n liora-prod port-forward --address 127.0.0.1 svc/backend 18080:8000
kubectl -n liora-prod port-forward --address 127.0.0.1 svc/frontend 18082:80
python3 docs/environment-evidence/probes/proxy.py
# The saved probes document the exact test fixture paths and commands.
python3 docs/environment-evidence/probes/smoke.py prod
```

Frontend HTTP 200, `/api/v1/utils/health-check/` HTTP 200 with `true`, `/readyz` HTTP 200, bcrypt login/JWT and item creation/read all passed in both environments. Actual browser logins displayed their separate records. Synthetic dev item: `47a9e7c4-e71e-439a-9673-3fc37c6fc76c`; prod item: `6d417890-4bad-4ad4-a100-20c67b46736b`. [Dev HTTP](environment-evidence/dev-http.json) · [Prod HTTP](environment-evidence/prod-http.json).

## Environment-isolation acceptance

Both database instances stayed running briefly while only one environment's web stack ran at a time. From the active backend, `socket.create_connection(('postgres', 5432))` succeeded, while the other namespace's `postgres.<namespace>.svc.cluster.local` connection was rejected. Both database targets passed `pg_isready`, and each backend's own connection was a positive control. The observed cross-namespace result was `ConnectionRefusedError`, consistent with rejection; no timeout was invented.

The other environment's credentials returned HTTP 400, and its item ID returned HTTP 404 using the active environment's valid JWT. Secret values were compared only in memory and all four credential values differed. Separate Secret UIDs, ConfigMaps, Services and PVC volume identities were recorded. After stopping prod web and restoring dev, dev frontend, health, readiness and the original record all returned HTTP 200. [Isolation results](environment-evidence/isolation-summary.txt) · [dev recheck](environment-evidence/dev-recheck.json).

Initial test-fixture problems are preserved in [setup corrections](environment-evidence/setup-corrections.txt): `.invalid` test emails were rejected by the application's validator and were changed to reserved `example.com` addresses; a stopped local proxy was restarted before browser validation. These transient failed attempts are not presented as passing tests.

## New screenshots and provenance

All 51 existing screenshots, including E19, remain byte-for-byte unchanged. Their dated metadata is preserved. If a source document changes, the evidence generator freezes the exact older source bytes under `presentation-evidence/historical-sources/` instead of silently reattributing an old screenshot to a new document. The extension catalog records dates, commands, scope, revisions and source hashes for the 11 new captures.

| ID | Screenshot | What it proves |
| --- | --- | --- |
| E52 | [Successful main pipeline](screenshots/05-automate-deployment-ci-cd-pipeline/E52.jpg) | Actual GitHub workflow: tests/scans/publication/dev promotion passed. |
| E53 | [Dev application](screenshots/02-deploy-the-application-in-multiple-environments-dev-prod/E53.jpg) | Actual authenticated UI with the dev database record. |
| E54 | [Dev readiness](screenshots/02-deploy-the-application-in-multiple-environments-dev-prod/E54.jpg) | Saved actual Kubernetes readiness, Services, PVC and Ingress metadata. |
| E55 | [Dev HTTP checks](screenshots/02-deploy-the-application-in-multiple-environments-dev-prod/E55.jpg) | Saved successful health/readiness/login/CRUD assertions. |
| E56 | [Prod application](screenshots/02-deploy-the-application-in-multiple-environments-dev-prod/E56.jpg) | Actual authenticated production-mode UI with a different record. |
| E57 | [Prod readiness](screenshots/02-deploy-the-application-in-multiple-environments-dev-prod/E57.jpg) | Saved actual prod readiness and independent storage. |
| E58 | [Prod HTTP checks](screenshots/02-deploy-the-application-in-multiple-environments-dev-prod/E58.jpg) | Saved successful production health/readiness/login/CRUD assertions. |
| E59 | [Isolation controls](screenshots/02-deploy-the-application-in-multiple-environments-dev-prod/E59.jpg) | Both directions of DB, credential and record isolation. |
| E60 | [Image identities](screenshots/01-dockerize-your-application/E60.jpg) | Published immutable digests match both environments' running pods. |
| E61 | [Configuration separation](screenshots/02-deploy-the-application-in-multiple-environments-dev-prod/E61.jpg) | Actual runtime config, distinct Secret objects and PVCs; no secret values. |
| E62 | [Render/policy checks](screenshots/02-deploy-the-application-in-multiple-environments-dev-prod/E62.jpg) | Both overlay checks and unchanged automatic-dev/manual-prod policy. |

E52/E53/E56 are actual UIs. The other eight additions are explicitly labeled **archived actual output**, captured immediately after verification and before cluster deletion. They are not live-terminal screenshots. All ten official requirement headings remain unchanged; [the evidence review](environment-evidence/all-requirements-review.md) records why earlier Docker/test/IaC/monitoring/security/recovery/documentation evidence was retained rather than restarting those stacks just for pictures.

[Final verification summary](environment-evidence/verification-summary.txt) · [offline Trivy secret scan](environment-evidence/evidence-secret-scan.txt) · [artifact SHA-256 checksums](environment-evidence/checksums.json). Three existing promotion regression tests and the new immutable-production CI guard passed locally.

## Cleanup and remaining work

The cluster, its synthetic databases, port-forwards, local proxy/viewer and generated credentials were removed after capture. No unrelated containers, volumes or clusters were deleted. [Cleanup audit](environment-evidence/cleanup.json). Minimum sampled available RAM was 1667 MiB; the guard was restarted when its process ended, so this is not a claim of uninterrupted monitoring. [Memory observations](environment-evidence/memory-summary.json).

**NOT YET TESTED:** public DNS/TLS, cloud provisioning, concurrent full web stacks, canonical production Argo manual synchronization, monitoring ServiceMonitor discovery/receiver delivery, off-site/etcd/replacement-host recovery and image/schema downgrade. The `.invalid` ingress hosts and TLS Secret reference are deliberately unchanged. Before public use, obtain authorized DNS/certificates, configure and verify TLS, and complete the remaining operational checks. Normal production release remains reviewed pins merged to main followed by an authorized manual Argo sync.
