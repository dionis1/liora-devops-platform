# Local validation report

Date: 22 October 2026 (Europe/Tirane).

**LOCAL VALIDATION RESULT: NOT READY FOR CLOUD DEPLOYMENT.**

All ten phases were assessed in order. Backend tests, image builds, a live dev
deployment, monitoring health checks, and a disposable database restore passed.
Security policy checks and private GitOps reconciliation failed. No Hetzner
resources were provisioned, no changes were pushed, and no user branches were
merged. Generated credentials, kubeconfigs and database dumps were not added to Git.

## Scope and source provenance

- Repository: https://github.com/dionis1/liora-devops-platform
- Inspected main commit: 3ca992543988c25ba644f130f06dcb1289f38a51.
- Original DataScientest submodule: f3c874cc0f4951b422b883b26a1ceef6cad141aa.
- Local branch: testing/local-validation-2026-10-22.
- Directory: /home/dionis/backup/liora-devops-platform.

**Acquisition limitation:** the private repository could not be cloned by the
command-line Git client: the restricted attempt could not resolve GitHub, and
the approved network attempt lacked Git authentication. The connected GitHub
app could read it. All 36 source blobs were fetched at the inspected revision,
verified against their Git blob SHA-1 hashes, and written into a new local
snapshot repository. The real submodule gitlink was preserved and
git submodule update --init --recursive successfully cloned the original app.
The local baseline commit is explicitly a snapshot, not the upstream Git history.

Do not push this snapshot branch as a replacement for upstream history. Apply
the accompanying [fixes patch](local-validation-fixes.patch) to an authenticated
clone at the inspected revision after checking it with git apply --check.
The application submodule has no local source changes. Platform-owned
Dockerfiles package that same application.

Evidence: [source hashes and CI job details](local-validation-evidence/provenance.json),
[security findings](local-validation-evidence/security-findings.json), and
[execution logs](local-validation-evidence/).

## Phase 1 — System readiness

| Item | Observation |
|---|---|
| OS / architecture | Ubuntu 24.04.5 LTS, x86_64 |
| CPU | Intel Core i5-10300H at 2.50 GHz; 8 logical CPUs |
| RAM | 7,777 MiB total; 1,523 MiB available initially |
| Swap | 8,191 MiB total; 4,273 MiB used initially |
| Disk | 468 GiB filesystem; 213 GiB available initially; approximately 208 GiB after validation |
| Later memory | Approximately 4.5 GiB available before live phases; about 3.0 GiB remained available during monitoring |
| Existing services | Four simple-admin containers: app, worker, PostgreSQL 17 and Redis |

Installed versions: Docker client/server 29.1.3; Compose 2.40.3; Python 3.12.3;
Git 2.43.0; Terraform 1.16.6; Ansible core 2.16.3; kubectl 1.35.9 with Kustomize
5.7.1; Helm 4.3.1; k3d 5.9.0 (default k3s 1.35.5-k3s1); uv 0.13.1;
Node 20.5.1; npm 10.2.0.

Needed additions: uv obtained Python 3.10.12 and the upstream frozen dependency
environment for backend tests. Missing Buildx 0.30.1 was downloaded as an Ubuntu
package and unpacked under /tmp/liora-validation, without a system package
installation. Use DOCKER_CONFIG=/tmp/liora-validation/docker to select it.
Trivy 0.76.1 was downloaded into that directory and its release SHA-256 verified.

Docker, snap tools, Terraform plugin sockets and network access were restricted
inside the execution sandbox; approved commands outside that restriction worked.
Ansible used ANSIBLE_LOCAL_TEMP=/tmp/liora-ansible-check. These access errors were
environment limitations, not application failures.

**Strategy:** remeasure RAM before each stack; require at least 3 GiB available
for a live cluster; use one server, zero agents, no load-balancer container and a
2 GiB server memory cap. Run builds and scans sequentially. Never stop unrelated
services, prune shared Docker storage, or use an existing Kubernetes context.

## Phase-by-phase results

PASS means observed success; FAIL means an observed failure or an unmet safety
gate; SKIPPED means not executed, with its reason given.

### Phase 2 — Static infrastructure

| Test | Result | Evidence / limitation |
|---|---|---|
| Terraform recursive formatting | FAIL → PASS | main.tf and variables.tf reformatted; final check passes |
| Terraform init, backend disabled | PASS | hcloud 1.68.0 downloaded; provider lockfile generated; no cloud API provisioning |
| Terraform validate | PASS | Provider schema validation succeeded |
| Infrastructure YAML syntax | PASS | All 18 original platform YAML files parsed |
| Ansible syntax | PASS | prepare.yml, k3s.yml, kubeconfig.yml |
| Example inventory | PASS | k3s_servers resolves to k3s-01 |
| k3s configuration review | PASS, static only | Version variable, embedded etcd, secret encryption and remote kubeconfig mode present |
| Dev / prod Kustomize rendering | PASS | Both rendered initially and after fixes |
| Final structural assertions | PASS | Namespace, selectors, ports, ConfigMap values, probes, memory bounds, token automount and local-path PVC references |
| Secret / registry configuration | PASS, references only | Local app credentials exercised in phase 5; private GHCR authentication not supplied |
| Deployment placeholders | FAIL deployment gate | Main overlays retain sha-bootstrap and example.invalid hosts; deploy/dev has published SHA tags |
| Production TLS | FAIL deployment gate | Ingress has no TLS configuration or certificate provisioning |

No cluster connection was made during phase 2. The deployment and DNS
placeholders were overridden only in temporary local test manifests.

### Phase 3 — Original backend

| Test | Result |
|---|---|
| Frozen dependencies, Python 3.10 | PASS |
| mypy / Ruff lint / Ruff formatting | PASS; 38 source files |
| PostgreSQL and test mail service startup | PASS; isolated Compose project, 256 MiB / 128 MiB limits, loopback ports |
| Database initialization and Alembic | PASS; all four migrations and initial data creation |
| Existing unit / CRUD / PostgreSQL integration / API tests | PASS; 55 passed, 2 SQLAlchemy warnings |
| Upstream coverage report | PASS; reported total 94%, including test modules in its denominator |
| Running FastAPI health endpoint | PASS; HTTP 200, body true |
| Cleanup | PASS; server process, containers and project network removed |

Tests used PostgreSQL 12, matching the original upstream Compose configuration,
and generated test credentials. They did not use any existing PostgreSQL data.
Email-dependent tests use the upstream mocks; real email delivery was not proved.
The health route is a process-level check and does not independently prove
database availability.

### Phase 4 — Docker images

Both original images built successfully, followed by both platform images.
Each image was smoke-tested separately, with a 512 MiB cap and no external
network. Test containers were removed immediately.

| Image | Original Docker-reported size | Final size after security fixes | Final runtime UID |
|---|---:|---:|---:|
| Backend | 491,363,071 bytes | 81,101,912 bytes | 10001 |
| Frontend | 64,148,302 bytes | 27,158,171 bytes | 101 |

PASS: Linux/amd64 builds, startup, backend health, frontend HTML serving, runtime
UID checks, and health-check commands. Other architectures were SKIPPED.
Final OS-patched images were rebuilt and smoke-tested again in phase 8.

The backend now uses a build stage and slim runtime, frozen dependencies without
development tools, one worker, a non-root user and a Python health check.
The frontend uses npm ci, a non-root Nginx 1.30 runtime, port 8080 and a wget
health check. Upstream source and Dockerfiles remain unchanged. CI selects the
platform Dockerfiles; Kubernetes Service port 80 targets frontend port 8080.

Strict reproducibility is not established: base image tags and OS package
repositories can change. Pin reviewed image digests and record rebuild inputs
before publishing a controlled release.

### Phase 5 — Live local Kubernetes

**PASS:** one temporary k3d server, zero agents, 2 GiB cap; dev namespace;
generated app Secret; PostgreSQL 16.10 StatefulSet; bound 8 GiB local-path PVC;
backend migration init container; ready backend and frontend Deployments;
Services; backend and frontend HTTP access through loopback port-forwards; and
Traefik host/path routing for both API and UI. Application pods had zero restarts
at the recorded readiness snapshot.

The temporary manifest used locally imported hardened images, a
dev.validation.test host, lower test memory limits and no GHCR pull secret.
This validates the dev deployment with those local adaptations, not unchanged
placeholder overlays or a private registry pull.

This cluster used the initial hardened images. The later OS/Nginx security
updates passed Docker smoke tests, but were not redeployed into Kubernetes.

The full 55-test suite was run against PostgreSQL 12 in phase 3; PostgreSQL 16
was validated here for initialization, migrations and deployment startup.
Production deployment, production DNS/TLS and end-to-end browser login were
SKIPPED. The cluster, image import volume and disposable database storage were
deleted before phase 6.

### Phase 6 — Argo CD

PASS: chart rendering and live isolated installation, argo-cd chart 10.10.5,
application version v3.5.5; loopback health endpoint HTTP 200; Application CRDs
accepted both checked-in Application resources.

PASS, configuration: dev tracks deploy/dev with automated sync, prune and
self-heal; production tracks main and has manual sync. Both source branches
exist. Production does not require a separate deploy/prod branch in this design.
Dev image tags reference sha-3ca992543988c25ba644f130f06dcb1289f38a51;
main's production tags remain bootstrap placeholders.

**FAIL:** both Applications reported ComparisonError / authentication required:
Repository not found. No read-only private-repository credential was configured.
Argo's health endpoint being healthy does not mean either application deployed.
Automatic dev sync, production sync, private GHCR access and live GitOps rollback
are SKIPPED pending credentials and deployable manifests. The Git-based rollback
runbook was reviewed; image rollback does not reverse database migrations.
The Argo cluster was deleted.

### Phase 7 — Monitoring

PASS: kube-prometheus-stack 92.11.0 rendered 112 objects and installed alone in a
separate 2 GiB cluster. Grafana, Prometheus and Alertmanager returned HTTP 200;
Prometheus returned 13 up samples, of which 12 were healthy. Prometheus storage
was provisioned through local-path. All components were removed with the cluster.

Failures investigated and corrected:

1. A test-harness cluster name exceeded k3d's 32-character limit; shortened.
2. Grafana sidecars OOM-killed at 64 MiB; changed to 192 MiB each.
3. Grafana core stalled at its 192 MiB ceiling: measured 191.9 MiB working set and
   about 1.5 CPU cores of sustained activity. Raising its cap to 384 MiB allowed
   readiness and HTTP health to pass. Sidecars then ran without restarts.
4. The first installation timeout was increased to allow image downloads and
   retesting. Final saved values were re-rendered and checked against the
   live-tested limits.

**FAIL / remaining:** Grafana's own metrics target was 0 in the first observed
scrape after startup. Its health endpoint passed, but a later successful scrape
was not captured. A startup timing explanation is plausible, not proven.

SKIPPED: application request/error/latency metrics, because the upstream app has
no Prometheus instrumentation or /metrics route. A minimal platform-owned
instrumentation wrapper and internal ServiceMonitor are proposed in
monitoring/README.md; they are not implemented.

SKIPPED: firing/resolved notification delivery, because no real Alertmanager
receiver was configured. Grafana persistence is disabled and Alertmanager state
is ephemeral. Configure durable storage and off-node backups before relying on
their settings or silences. Appropriate alerts include pod crash loops, replica
unavailability, scrape failures, an independent application-health probe, and
API 5xx ratios after instrumentation exists.

### Phase 8 — Security

Trivy scans ran one at a time with parallelism 1. Counts below are findings per
package/artifact occurrence, not unique exploitable vulnerabilities.

| Scan | Critical | High | Result |
|---|---:|---:|---|
| Upstream source dependencies, excluding dev dependencies | 5 | 36 | FAIL |
| Source including development dependencies | 9 | 70 | FAIL |
| Source configuration | 0 | 7 | FAIL; separate from dependency counts |
| Hardened backend, final | 4 | 67 | FAIL |
| Hardened frontend before OS fixes | 3 | 66 | FAIL |
| Hardened frontend, final Nginx 1.30 + OS updates | 0 | 0 | PASS for the requested HIGH/CRITICAL image scan |

The backend's final count comprises 4 critical / 23 high Python findings with
reported fixes and 44 high Debian findings without a fixed version reported.
An OS update rebuild did not clear those findings. Frontend image scanning does
not establish that bundled JavaScript is vulnerability-free; source lockfile
findings remain.

Database, Kubernetes control-plane, Argo CD and monitoring images were not
included in these local vulnerability scans. A complete stack image audit
remains open.

Representative critical dependency findings:

| Package | Installed | Reported fixed version | Identifier |
|---|---|---|---|
| anyio | 4.6.0 | 4.14.2 | CVE-2026-63374 |
| certifi | 2024.8.30 | 2026.10.19 | GHSA-6q48-6c7w-9gw2 |
| h11 | 0.14.0 | 0.16.0 | CVE-2025-43859 |
| PyJWT | 2.9.0 | 2.14.0 | CVE-2026-102268 |
| form-data | 4.0.0 | 4.0.4 on the same major line | CVE-2025-7783 |

Development dependency critical findings also include handlebars and tar.
The sanitized security evidence contains all scanned identifiers and fixed
versions. Dependency findings were not silently suppressed or described as
fixed. Updating the upstream dependency locks requires a compatible dependency
update, full backend retest and frontend verification; that work remains open.

| Severity | Finding / action |
|---|---|
| Critical | Unresolved upstream Python/JavaScript dependency advisories; block deployment until updated or individually assessed |
| High | Backend image remains above policy thresholds; no blanket exception was added |
| High | Production ingress has no TLS; configure certificates and HTTPS before public exposure |
| High | No application NetworkPolicies; namespaces alone do not provide network isolation |
| High, scanner | Writable root filesystems in four app/init containers, plus root-user checks for three unchanged upstream Dockerfiles |
| Medium | Private GitOps credentials and GHCR pull credentials not validated |
| Medium | Health check does not independently test database readiness; app metrics and alert delivery remain unverified |
| Medium | Existing k3s binary bypasses version enforcement in Ansible; upgrades need a reviewed procedure |
| Medium | Branch-list metadata reports main unprotected; review branch rules before production promotion |
| Low | Action tags and base image tags are mutable; use reviewed immutable references for controlled releases |

Implemented controls: non-root platform images; dropped capabilities and disabled
privilege escalation for backend/frontend; RuntimeDefault seccomp; disabled
service-account token automount for app/database pods; migration resource bounds;
startup probe; explicit controller secrets directory 0700 / kubeconfig 0600;
weekly submodule update checks; source scan failure status; source and published
image scan gates before dev promotion. No high/critical secret matches were
reported in the scanned files. This was not a full-history or all-severity secret
audit, and no secret-free-history claim is made.

New CI gates are locally syntax/structure-checked but have not run remotely.
They intentionally remain failing while actionable findings are unresolved.

### Phase 9 — Disaster recovery

PASS: all three shell scripts pass bash syntax checks. A disposable PostgreSQL
12 container held three marker records. The repository backup script executed a
real pg_dump custom-format dump through a strictly scoped kubectl shim that
forwarded only the expected command to that container. pg_restore --list read
the archive; pg_restore --exit-on-error restored it into a NEW database; all
three restored records matched. This validates the dump/restore commands and
script behavior, not Kubernetes transport or a PostgreSQL 16 restore.

PASS: backup mode 0600; invalid namespaces rejected; a simulated partially
written failed dump left no completed archive or temporary file.

Fix: set umask before creating the backup directory, write to a unique temporary
file, and atomically publish only a successful nonempty dump without replacing
another backup. BACKUP_DIR allows a disposable destination. Restore documentation
now uses --exit-on-error.

SKIPPED: embedded-etcd snapshot/restore execution, PVC/node-loss recovery,
off-site encryption/retention/RPO/RTO drills, Terraform cloud recreation,
Ansible replacement-host recreation and live GitOps rollback. The runbooks cover
off-node snapshots, the k3s token, Terraform state, secrets and migration
compatibility, but procedures alone are not recovery evidence.

The test container was removed. No existing database was restored over or deleted.

### Phase 10 — CI and final audit

Existing remote evidence at the inspected main commit:

- [FastAPI CI run 39802778100](https://github.com/dionis1/liora-devops-platform/actions/runs/39802778100):
  backend lint, PostgreSQL tests, GHCR publication of both images and dev promotion succeeded.
- [Platform validation run 39802778090](https://github.com/dionis1/liora-devops-platform/actions/runs/39802778090):
  Terraform, Ansible and Kustomize jobs succeeded.
- [Security run 39802778052](https://github.com/dionis1/liora-devops-platform/actions/runs/39802778052):
  workflow succeeded, but its checked-in exit-code was 0. This is execution
  evidence, not evidence of a clean security scan.

Fix: the old promotion logic only edited image tags on an existing deploy/dev
branch, allowing its platform manifests to remain stale. The proposed workflow
merges the validated main commit before changing tags and fails on conflicts.
A disposable Git fixture tested this with merge-tree, preserving the prior dev
tag while bringing the new platform configuration forward. No user branch was
actually merged and no workflow was dispatched.

Final checks PASS: Terraform formatting/validation; both final Kustomize
renders and structural assertions; final monitoring limits; modified Ansible
syntax; all three workflow YAML documents and embedded shell scripts; git diff
--check. Remote execution of local workflow edits is SKIPPED because nothing
was pushed.

## Commands executed

Routine source reads, Git status checks and memory samples accompanied each phase.
The substantive commands and local harnesses were:

~~~bash
free -m
nproc
df -h /home/dionis/backup /tmp
docker version
docker compose version
docker ps
docker info
git --version
python3 --version
terraform version
ANSIBLE_LOCAL_TEMP=/tmp/liora-ansible-check ansible-playbook --version
kubectl version --client
helm version --short
k3d version
uv --version
node --version
npm --version
git clone https://github.com/dionis1/liora-devops-platform.git
git submodule update --init --recursive
terraform fmt -check -recursive
terraform fmt -recursive
terraform -chdir=infrastructure/terraform init -backend=false -input=false
terraform -chdir=infrastructure/terraform validate -no-color
ansible-playbook -i ansible/inventory/hosts.ini.example --syntax-check ansible/playbooks/prepare.yml
ansible-playbook -i ansible/inventory/hosts.ini.example --syntax-check ansible/playbooks/k3s.yml
ansible-playbook -i ansible/inventory/hosts.ini.example --syntax-check ansible/playbooks/kubeconfig.yml
ansible-inventory -i ansible/inventory/hosts.ini.example --graph
kubectl kustomize kubernetes/overlays/dev
kubectl kustomize kubernetes/overlays/prod
uv sync --frozen --python 3.10
uv run --frozen --python 3.10 bash scripts/lint.sh
uv run --frozen --python 3.10 bash scripts/prestart.sh
uv run --frozen --python 3.10 bash scripts/tests-start.sh
apt-get download docker-buildx
docker build -t liora-validation-backend:20261022 course-app/backend
docker build --build-arg VITE_API_URL= -t liora-validation-frontend:20261022 course-app/frontend
docker build -f docker/backend.Dockerfile -t liora-validation-backend:hardened course-app/backend
docker build -f docker/frontend.Dockerfile -t liora-validation-frontend:hardened course-app/frontend
docker image inspect IMAGE
python3 /tmp/liora-validation/backend-check.py lint
python3 /tmp/liora-validation/backend-check.py up
python3 /tmp/liora-validation/backend-check.py migrate
python3 /tmp/liora-validation/backend-check.py tests
python3 /tmp/liora-validation/backend-check.py smoke
python3 /tmp/liora-validation/backend-check.py down
python3 /tmp/liora-validation/image-smoke.py
python3 /tmp/liora-validation/kubernetes-check.py
python3 /tmp/liora-validation/argocd-check.py
python3 /tmp/liora-validation/monitoring-check.py
python3 /tmp/liora-validation/image-smoke-final.py
python3 /tmp/liora-validation/dr-check.py
git merge-tree --write-tree deploy/dev main
git diff --check
~~~

Docker builds used the temporary Buildx DOCKER_CONFIG, unique image tags,
validation labels and plain progress logs. Initial --progress failed before
Buildx was available. Backend commands ran from course-app/backend with a private
generated environment. The backup harness used a private --env-file rather than
literal passwords. No generated credential values are included here.

Cluster harnesses execute k3d cluster create with --servers 1 --agents 0
--servers-memory 2048m --no-lb, loopback API ports 16550–16552, disabled default
kubeconfig updates, and bounded startup waits. They obtain a dedicated kubeconfig,
use explicit kubectl contexts, wait for rollouts, run loopback HTTP checks, and
delete only the named test cluster in finally blocks. Argo/monitoring disable
Traefik and metrics-server. Application testing keeps Traefik.

Helm used isolated HELM_CACHE_HOME / HELM_CONFIG_HOME / HELM_DATA_HOME paths,
helm show chart, helm template, and helm install --wait with pinned versions
10.10.5 (Argo CD) and 92.11.0 (monitoring). Diagnostic commands included scoped
kubectl get pods/events/pvc/services, logs, a kubelet stats summary, and targeted
Grafana resource patches. The saved values match the tested final limits.

Trivy commands used --cache-dir /tmp/liora-validation/trivy-cache --parallel 1
--timeout 5m --severity HIGH,CRITICAL --format json. Source scans used fs
--scanners vuln,misconfig,secret, with .git, .venv, htmlcov and Terraform provider
directories excluded; the final source policy run added --include-dev-deps and
--exit-code 1 and failed. Image scans used image --image-src docker --scanners
vuln, one image at a time. Image collection commands return 0 by default even
when findings exist; their policy results above come from the JSON findings.

GitHub read-only API calls obtained repository metadata, the recursive source
tree, pinned file contents, branch metadata, deploy/dev tags, workflow runs and
job results. Public release metadata supplied the verified Trivy download.

## Files changed

- .github/workflows/ci.yml: platform image builds, security gates and current-manifest dev promotion.
- .github/workflows/security.yml: non-persisted checkout credentials and failing scan policy.
- .github/workflows/validate-platform.yml: enforce Terraform formatting checks.
- .github/dependabot.yml: original submodule update checks.
- docker/backend.Dockerfile and docker/frontend.Dockerfile: tested platform packaging and OS updates.
- infrastructure/terraform/main.tf and variables.tf: formatting.
- infrastructure/terraform/.terraform.lock.hcl: provider checksums.
- ansible/playbooks/kubeconfig.yml: controller credential file permissions.
- kubernetes/base/backend.yaml: non-root security controls, startup probe and init limits.
- kubernetes/base/frontend.yaml: port 8080 and non-root security controls.
- kubernetes/base/database.yaml: disabled token automount and seccomp.
- monitoring/kube-prometheus-stack-values.yaml: explicit tested memory budgets.
- monitoring/README.md: tested chart pin, state limits, metrics and alert proposal.
- scripts/backup-postgres.sh: private, atomic, failure-safe backups.
- docs/disaster-recovery.md: fail-fast restore command.
- README.md and docs/architecture.md: current packaging, gates and report links.
- docs/local-validation-report.md, local-validation-fixes.patch and local-validation-evidence/: audit artifacts.

## Requirements compliance

| Requirement | Assessment |
|---|---|
| 1. Dockerization and registry | PASS local builds/runtime; existing CI publication evidence; private pull not tested |
| 2. Dev and production environments | PARTIAL: separated overlays/configurations; only dev deployed locally; production placeholders/TLS unresolved |
| 3. Application tests | PASS: original 55 tests, lint, migrations and health; frontend browser E2E not run |
| 4. Kubernetes orchestration | PASS for adapted local dev; cloud production remains unverified |
| 5. Working CI/CD | PARTIAL: existing CI passes; private Argo reconciliation fails; new workflow edits unrun remotely |
| 6. Terraform IaC | PASS static; cloud plan/apply/recreation not run |
| 7. Monitoring | PARTIAL: live cluster metrics and UI health; Grafana self-scrape, app metrics, notifications and durable settings incomplete |
| 8. DevSecOps | FAIL policy: unresolved critical/high findings; several controls implemented and retested |
| 9. Disaster recovery | PARTIAL: disposable SQL backup/restore passed; node/etcd/off-site/full-platform recovery unverified |
| 10. Documentation and diagram | PASS presence and updates; architecture Mermaid diagram and runbooks reviewed |

## Remaining deployment gates

Before any public deployment: remediate or individually assess the recorded
dependency vulnerabilities; rebuild and rescan; verify both application tests
and frontend behavior after dependency updates; establish authenticated Git
access and backport these changes into real history; run the revised CI;
configure read-only Argo repository access and namespace GHCR pull credentials;
promote real SHA-tagged images; configure DNS/TLS and network policy; confirm all
scrapes; implement app metrics and test alert delivery; and configure durable,
encrypted off-node recovery with a demonstrated restore.

Tests specifically deferred to the future Hetzner environment include provider
plan/apply and real network/firewall access, Ubuntu/Ansible bootstrap, actual
server sizing, public ingress/TLS, node/PVC failure, embedded-etcd restoration
with the server token, and full replacement-server recovery. No such commands
were executed. Some can also be rehearsed on an isolated Ubuntu VM.

Private GitOps sync, registry access, frontend E2E, dependency remediation,
notification tests and the new GitHub workflow runs do not inherently require
Hetzner; they remain local/CI prerequisites rather than reasons to buy a server.

## Cleanup and terminal summary

All validation containers, temporary application/Argo/monitoring clusters,
their disposable storage, tracked port-forward processes, and four validation
image tags were removed. The four original simple-admin containers remained
running with their original IDs. Existing stopped flagship-platform and
gitlab-gitops clusters were left untouched.

Shared Docker build caches, base images, the backend virtual environment,
downloaded temporary tools and sanitized audit logs were retained; no broad
pruning or unrelated-data deletion was performed. They consume disk but do not
run services. Generated test credential files, kubeconfigs and disposable dump
files were removed after evidence was collected.

**LOCAL VALIDATION RESULT**

- Passed: 55 backend tests; lint; four migrations; Terraform/Ansible/Kustomize; original and final image builds/smokes; adapted live dev Kubernetes; Argo server health; monitoring health and 12 successful scrape targets; disposable SQL restore.
- Failed: source/backend security policy; private GitOps authentication; production TLS/image/DNS gates; Grafana self-scrape not confirmed successful.
- Skipped due to RAM: 0 final tests; tight monitoring limits caused failures that were investigated and corrected.
- Fixed: Terraform format enforcement; missing temporary Buildx; image privileges/packaging/health checks; frontend image high/critical vulnerabilities; Kubernetes security/resource settings; Grafana memory limits; kubeconfig permissions; scan gates; stale dev manifests; atomic backup handling.
- Still needs Hetzner: real provisioning/bootstrap, public networking/TLS and full server/etcd/PVC/off-site recovery validation.
- Ready for cloud deployment: **NO**.


## Second validation pass

The first-pass evidence above is preserved. See [the remediation report](remediation-report.md) for dependency fixes, the authenticated Git history, current security blockers, and new screenshots. Historical results above are not assertions that the hardened second-pass manifests have passed a new cluster run.
