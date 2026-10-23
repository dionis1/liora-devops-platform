# Second validation result — 2026-10-23

**Superseded backend security result:** The later [Alpine backend remediation](backend-security-remediation.md) passes the strict local image gate with 0 HIGH / 0 CRITICAL and exact-image PostgreSQL integration checks. The results below describe the earlier Debian pass and are preserved as historical evidence. Cloud/Kubernetes/Argo gaps remain.

This pass preserved the first validation, fixed dependencies and delivery gates, and captured five real UI screenshots. No Hetzner resources were provisioned. The project is **not ready for public production deployment**: the backend OS image still violates the HIGH security policy, and hardened cluster/GitOps/cloud checks remain incomplete.

| Requested result | Observed result |
| --- | --- |
| Previous fixes preserved | **YES** — 50 prior changed/evidence files compared byte-for-byte before further edits; original report and patch retained |
| FastAPI tests | **PASS** — 55 upstream tests against disposable PostgreSQL 16.10; 2 platform metrics/readiness tests; mypy/Ruff pass |
| Docker backend | **PASS build and health/metrics smoke**; security gate **FAIL** |
| Docker frontend | **PASS** — TypeScript, Vite production bundle, image build, read-only runtime and actual login-page render |
| Critical findings remaining | **0** in patched dependency locks and both final runtime images |
| High findings remaining | **44** in backend Debian packages, all without a FixedVersion; **0** Python/frontend lock or frontend runtime HIGH findings |
| Terraform / Ansible | **PASS** — formatting, backend-free initialization/validation and three syntax checks; no apply/install |
| Local Kubernetes | **SKIPPED in this pass** — available RAM below the 3 GiB gate; first-pass deployment PASS remains historical evidence |
| Argo CD GitOps | **SKIPPED live reconciliation** — exact temporary SSH key reads real private GitHub, but read-only scope unverified; no new dev sync/rollback or GHCR pull proof |
| Prometheus / Grafana | **PASS isolated Docker validation** — 3/3 targets UP including Grafana, real dashboard values, unavailable alert firing then clearing; new Helm/ServiceMonitor runtime integration untested |
| PostgreSQL backup/restore | **PASS** — real PG16 custom dump, fresh restore, 3 matching rows, mode 0600, failed-dump cleanup and namespace rejection |
| GitHub changes committed | User-authorized testing-branch commit; see Git history for final SHA |
| Pull request ready | Draft review is appropriate; remaining security/runtime gates prevent release approval |
| Safe to begin cloud infrastructure testing | **NO as a deployment-ready release**; resolve image policy and credential/runtime gates first |
| Ready for public production deployment | **NO** |

## Provenance and preservation

The authentic GitHub `main` revision was `3ca992543988c25ba644f130f06dcb1289f38a51`.
The remediation branch is `testing/remediation-2026-10-22`, created from that history.
The reconstructed first-pass snapshot was preserved separately and was never used as a push parent.
The original DataScientest submodule remains pinned to `f3c874cc0f4951b422b883b26a1ceef6cad141aa` with MIT attribution.
See [preservation comparison](remediation-evidence/preserved-first-pass.json), [original report](local-validation-report.md), and [original patch](local-validation-fixes.patch).

## Reviewed application integration

The root-owned [patch](../patches/course-app-platform.patch) keeps dependency and compatibility changes reviewable without publishing an inaccessible submodule commit. `bash scripts/prepare-course-app.sh` checks the pinned revision, refuses conflicting tracked edits, applies safely and detects an already-applied patch. Patch replay was checked against a clean checkout of the exact upstream revision.

Python 3.12 and a fresh uv lock replace the old vulnerable dependencies. FastAPI uses its standard extra without the unnecessary cloud CLI; Starlette 1.9 and Sentry 2 resolve previous issues. SQLAlchemy/typing compatibility and two ineffective startup mocks were corrected. A platform-owned ASGI wrapper imports the existing FastAPI app; it adds bounded request/status counters, response-duration histograms, `/metrics`, and database-backed `/readyz` with a two-second connection timeout. The public ingress exposes `/api`, not the internal metrics endpoint.

Frontend locks include current Axios/form-data, patched Vite 6 and compatible SWC plugin, updated Playwright, and explicit transitive security overrides. A nullable theme-selection callback required a small compatibility guard. A broad Zag override initially broke newer Chakra packages; narrowing it to the vulnerable legacy version restored the build. Tar 7 is a major transitive override: production build compatibility passed, but OpenAPI client regeneration and browser end-to-end suites were not exercised.

The exact new `scripts/test-backend.sh` was also run end to end: all 55 upstream tests and both platform tests passed, with its disposable database/network removed by the exit trap. Its generated admin password was shortened to fit the upstream 40-character limit. [CI script evidence](remediation-evidence/ci-backend-tests.txt).

[Backend test evidence](remediation-evidence/backend-tests.txt), [lint](remediation-evidence/backend-lint.txt), [platform tests](remediation-evidence/metrics-tests.txt), [backend build](remediation-evidence/backend-build.txt), [frontend build](remediation-evidence/frontend-build.txt).

## Security and CI

Trivy 0.76.1 scanned patched Python and npm locks including development dependencies, final runtime images, platform Dockerfiles, Kubernetes and Terraform configuration, and repository secrets. No CVEs were suppressed, and unfixed findings remain included. The unused original upstream development Dockerfiles/Compose examples were preserved and are outside the deployed-config misconfiguration scope. Zero HIGH/CRITICAL findings is not a claim about lower severities or unknown vulnerabilities.

| Scope | CRITICAL | HIGH |
| --- | ---: | ---: |
| Patched Python + frontend locks, including dev | 0 | 0 |
| Backend runtime | 0 | 44 |
| Frontend runtime | 0 | 0 |

All 44 remaining backend findings have no published fix in the scanned Debian release. Their identifiers, packages, versions, impact titles and advisory links are recorded in [the complete deferral inventory](remediation-evidence/backend-unfixed-findings.json). Deferral reason: the image already applies available OS upgrades; no fixed Debian version is listed. An alternative base requires its own compatibility and image validation. These remain **release blockers**, not accepted exceptions. See [scan counts and scope](remediation-evidence/security-summary.json).

CI now runs upstream lint/tests, platform validation, source gates and sequential image scans before GHCR publication. The publication job loads the exact scanned images from an artifact. Dev promotion merges the validated main manifests before setting SHA tags. Job-level permissions separate read-only builds, package publication and Git promotion. Production Argo sync remains manual. Workflows were parsed and scripts checked locally; GitHub-hosted execution remains a separate check. Strict backend scanning is expected to block publication while these 44 HIGH findings remain.

## Monitoring and screenshots

The [ServiceMonitor, alert rules](../monitoring/application-observability.yaml), [dashboard](../monitoring/dashboards/fastapi.json), and dashboard ConfigMap are implemented and render successfully. The dashboard uses the stable `liora-prometheus` datasource UID. Grafana's own ServiceMonitor is enabled in Helm values.

To respect the laptop memory budget, runtime monitoring used a separate loopback-only Docker fixture, not a second Kubernetes/Helm installation. It ran Prometheus 3.15.0 and Grafana 13.2.4 with memory caps; Grafana used the previously validated 384 MiB allowance. No database or full app stack ran alongside monitoring. The actual platform backend emitted metrics from 40 health requests and 40 deliberate 404s. All three targets (backend, Grafana, Prometheus) were UP. The provisioned dashboard showed request totals, errors, rate and latency.

The unchanged one-minute `LioraApplicationUnavailable` rule was syntax-checked with promtool, reached firing after the disposable backend stopped, and cleared after restart. Alertmanager notification delivery and the sustained 5xx rule were not runtime-tested. Configure a receiver and test firing/resolved delivery before relying on notifications. The screenshot fixture alone enabled anonymous Grafana Viewer access; platform Helm authentication still uses an admin Secret.

[Targets](remediation-evidence/monitoring-targets.json), [firing](remediation-evidence/alert-firing.json), [recovery](remediation-evidence/alert-resolved.json), [five screenshots and their scope](screenshots/README.md).

## Kubernetes, GitOps and remaining runtime gates

Workloads use non-root IDs, RuntimeDefault seccomp, read-only root filesystems, dropped ALL capabilities, no privilege escalation, disabled service-account token mounts and explicit CPU/memory limits. Writable temporary directories are bounded emptyDir mounts. PG16 UID/GID 999 and read-only-root operation were verified in the disposable Docker DR drill. Backend readiness checks the database. Namespaces enforce the restricted Pod Security profile; default-deny policies allow DNS, Traefik ingress, Prometheus scraping and backend-to-database traffic. External SMTP/Sentry egress requires an explicit allowlist. Production ingress references a configurable TLS Secret and placeholder host. These changes rendered and passed the HIGH/CRITICAL static config scan, but their combined live cluster behavior needs retesting.

The temporary key was tested with `-F /dev/null`, `IdentitiesOnly=yes` and `IdentityAgent=none`, and read the actual private GitHub HEAD. However, the repository deploy-key API listed zero keys. Therefore read-only access was **not verified**, and the key was not installed into Argo CD. Account-level access is not accepted as a substitute for a repository-specific read-only credential. See [auth evidence](remediation-evidence/argocd-auth-result.json) and [credential procedure](deployment.md#private-git-authentication-validation). Dev application synchronization, private GHCR pulls, rollback, and hardened network policy behavior remain untested in this pass. No local Git mirror was presented as GitHub-authentication proof.

Available RAM was approximately 1.7–3.0 GiB before monitoring, below the required 3 GiB cluster start gate. No new k3d cluster was started. Local HTTPS was therefore skipped; neither public TLS nor hardened Traefik ingress is claimed validated. Original successful first-pass Kubernetes evidence remains intact.

## Recovery and cleanup

The actual backup script was exercised through a temporary kubectl-to-Docker adapter against isolated PG16.10. A real custom archive restored into a new disposable database with all three marker rows matching. Dumps were mode 0600; simulated partial failure left no completed or temporary file, and invalid namespace input was rejected. No existing user database or volume was touched. [DR evidence](remediation-evidence/disaster-recovery.txt).

Embedded-etcd snapshot/token requirements were reviewed against [official K3s backup documentation](https://docs.k3s.io/datastore/backup-restore) and [restore instructions](https://docs.k3s.io/cli/etcd-snapshot). Actual server-token recovery, etcd restore, off-site durability, replacement-VM recovery, production DNS/TLS, firewall behavior and Hetzner API/network/storage behavior still require a real isolated server drill.

Temporary test containers and networks are removed after screenshots. Secrets, keys, dumps, Terraform state and kubeconfigs are excluded from the commit. The four pre-existing simple-admin containers and unrelated k3d clusters are left intact. The exact temporary key was identified as account-level SSH access and removed with explicit user approval; its absence was verified. See [key cleanup](remediation-evidence/key-cleanup.json). No cloud deployment, merge to main or force-push is part of this pass.


## Graduation evidence follow-up — 2026-10-23

The [presentation pack](presentation-evidence.md) now contains **38 screenshots**, organized by the exact ten official requirement titles: **12 actual UI captures** and **26 clearly labeled archived-output/configuration/design views**. All five original UI images were preserved byte-for-byte. The [manifest](screenshots/manifest.json) records dates, versions, scope, source links/hashes and image hashes. See [the final compliance report](final-compliance-report.md) for all ten assessments; evidence coverage is not a claim of ten successful deployments.

A small isolated Docker fixture (192 MiB backend, 64 MiB frontend, 256 MiB PG16) reused cached image layers and validated a real browser login, item creation and persistence after reload. API health and database readiness returned 200. A temporary Nginx `/api` proxy provided the same-origin UI/API routing in this Docker fixture; it is not a new Traefik/Kubernetes routing validation. The captured fixture YAML/proxy configuration is preserved without its credential file. The API/UI were then stopped; the actual atomic backup script was exercised via an explicitly documented kubectl-to-Docker adapter. A mode-0600 dump restored into a fresh database, with the exact same synthetic item ID/title visible in both databases and the earlier browser screenshot. Failed-dump cleanup passed. The fixture was removed after captures. Existing user containers were preserved.

The user made the GitHub repository public during evidence collection. Direct workflow screenshots now show the **historical 3ca9925 publication/promotion success**, **211199d test/lint/platform/source-scan successes**, and **211199d backend image gate failure with publication/promotion skipped**. Historical private Argo comparison failure is labeled as historical; new public-repository reconciliation is still NOT YET TESTED. No read-only deploy-key success is invented. GHCR package/tag metadata was unavailable without read:packages scope; no current registry pull or package-visibility change is claimed.

Both the eight-step live plan and exact ten-step screenshot-only fallback allocate **600 seconds**. The offline gallery has no external assets or scripts. The [capture-before-cleanup protocol](screenshots/capture-protocol.md) is mandatory for every remaining validation/remediation phase. A dated output/metadata capture is used when original terminal/cluster screenshots no longer exist. Final Kubernetes security-policy enforcement, production/public HTTPS, Argo sync/rollback, notification delivery, cloud infrastructure/recovery and actual k3s snapshots remain untested.
