# Official requirements validation checklist

Keep the exact official numbering. A checked execution item does not mean an entire requirement passed. Capture readable evidence before stopping a successful test.

## 1. Dockerize Your Application

**Assessment: PASSED**

- [x] Implementation documented: Multi-stage, non-root platform images around the original pinned DataScientest application; digest-pinned Alpine backend, health checks and a reviewed dependency patch.
- [x] Executed checks recorded: Sequential builds, actual API/database readiness, authenticated browser login, item creation and persistence after reload in a fixture with a temporary Nginx API proxy. Historical main publication succeeded.
- [x] Concrete evidence indexed: [E07: Browser-created item persists after reload](screenshots/01-dockerize-your-application/item-created-and-persisted.jpg), [E08: Executed Swagger request returns HTTP 200](screenshots/01-dockerize-your-application/swagger-real-health-200.jpg), [E13: Backend image build completed](screenshots/01-dockerize-your-application/E13.jpg), [E14: Frontend TypeScript and production bundle completed](screenshots/01-dockerize-your-application/E14.jpg), [E15: Running containers and health checks](screenshots/01-dockerize-your-application/E15.jpg), [E10: Historical successful GHCR publication and dev promotion](screenshots/05-automate-deployment-ci-cd-pipeline/github-historical-publish-promote.jpg).
- [ ] Remaining validation: Publication and authenticated registry pulls for the new Alpine backend are NOT YET TESTED. PR checks do not publish; publication/promotion require a validated push to main. Historical publication evidence is retained.

## 2. Deploy the Application in Multiple Environments (Dev & Prod)

**Assessment: PARTIALLY VALIDATED**

- [x] Implementation documented: Separate dev/prod namespaces, overlays, host settings, credentials references and a production TLS Secret reference.
- [x] Executed checks recorded: Both overlays render; first-pass dev deployment and routing ran locally.
- [x] Concrete evidence indexed: [E19: Dev and prod separation: static manifests](screenshots/02-deploy-the-application-in-multiple-environments-dev-prod/E19.jpg), [E20: Historical dev pods and Services READY](screenshots/04-container-orchestration-with-kubernetes/E20.jpg), [E21: Historical PVC and Kubernetes HTTP access](screenshots/04-container-orchestration-with-kubernetes/E21.jpg).
- [ ] Remaining validation: Production deployment and public TLS are NOT YET TESTED; final hardened dev manifests were not redeployed.

## 3. Run Tests on the Application

**Assessment: PASSED**

- [x] Implementation documented: Upstream tests, PostgreSQL migrations, mypy/Ruff, and metrics/readiness checks run in CI.
- [x] Executed checks recorded: 55 upstream tests and 2 platform tests pass; exact CI script passes locally and hosted backend-tests/lint jobs passed at 211199d. New browser login/create/reload smoke passed.
- [x] Concrete evidence indexed: [E16: 55 upstream tests passed](screenshots/03-run-tests-on-the-application/E16.jpg), [E17: Platform metrics and readiness tests passed](screenshots/03-run-tests-on-the-application/E17.jpg), [E18: Mypy and Ruff passed](screenshots/03-run-tests-on-the-application/E18.jpg), [E09: Historical Debian CI blocks publication](screenshots/05-automate-deployment-ci-cd-pipeline/github-current-security-gate.jpg), [E07: Browser-created item persists after reload](screenshots/01-dockerize-your-application/item-created-and-persisted.jpg).
- [ ] Remaining validation: The complete automated browser E2E suite and OpenAPI-client regeneration are NOT YET TESTED.

## 4. Container Orchestration with Kubernetes

**Assessment: PARTIALLY VALIDATED**

- [x] Implementation documented: Deployments, StatefulSet, PVC, Services, ConfigMap, Ingress, namespace policy and resource/security settings.
- [x] Executed checks recorded: Historical local dev pods reached 1/1 Ready, PVC Bound, rollouts completed, and frontend/backend/Traefik HTTP routing passed; new manifests render.
- [x] Concrete evidence indexed: [E20: Historical dev pods and Services READY](screenshots/04-container-orchestration-with-kubernetes/E20.jpg), [E21: Historical PVC and Kubernetes HTTP access](screenshots/04-container-orchestration-with-kubernetes/E21.jpg), [E37: Historical ConfigMap, Ingress and rollout results](screenshots/04-container-orchestration-with-kubernetes/E37.jpg), [E19: Dev and prod separation: static manifests](screenshots/02-deploy-the-application-in-multiple-environments-dev-prod/E19.jpg).
- [ ] Remaining validation: Historical cluster was deleted. Current hardened cluster, policy enforcement, node-readiness screenshot and cloud deployment are NOT YET TESTED.

## 5. Automate Deployment (CI/CD Pipeline)

**Assessment: PARTIALLY VALIDATED**

- [x] Implementation documented: Tests/build/scan gates, exact-scanned-image publication, dev manifest promotion and manual production sync policy; Argo Application manifests.
- [x] Executed checks recorded: Historical main publication/promotion passed. The Debian scan at 211199d failed with 44 HIGH findings. The new Alpine backend passes the strict local scan with 0 HIGH/CRITICAL and image integration checks; new hosted CI results must be checked separately. Historical Argo installed but private repo comparison FAILED.
- [x] Concrete evidence indexed: [E09: Historical Debian CI blocks publication](screenshots/05-automate-deployment-ci-cd-pipeline/github-current-security-gate.jpg), [E10: Historical successful GHCR publication and dev promotion](screenshots/05-automate-deployment-ci-cd-pipeline/github-historical-publish-promote.jpg), [E22: Argo CD ran, but private repository comparison failed](screenshots/05-automate-deployment-ci-cd-pipeline/E22.jpg), [E23: Production manual sync configuration](screenshots/05-automate-deployment-ci-cd-pipeline/E23.jpg), [E38: Historical Argo components ready; sync still unproven](screenshots/05-automate-deployment-ci-cd-pipeline/E38.jpg).
- [ ] Remaining validation: Successful Argo Synced/Healthy application, public-repo reconciliation and rollback are NOT YET TESTED. The repository became public on 2026-10-23; historical private auth errors do not establish a current public auth failure.

## 6. Create IaC (Infrastructure as Code) Templates

**Assessment: PARTIALLY VALIDATED**

- [x] Implementation documented: Terraform Hetzner templates and Ansible preparation/k3s/kubeconfig playbooks, with restricted SSH configuration.
- [x] Executed checks recorded: Fresh Terraform fmt/validate and three Ansible syntax checks passed; hosted platform validation passed.
- [x] Concrete evidence indexed: [E24: Terraform formatting and validation passed](screenshots/06-create-iac-infrastructure-as-code-templates/E24.jpg), [E25: Three Ansible syntax checks passed](screenshots/06-create-iac-infrastructure-as-code-templates/E25.jpg), [E11: Current Terraform, Ansible and Kustomize workflow passes](screenshots/06-create-iac-infrastructure-as-code-templates/github-platform-validation-passed.jpg).
- [ ] Remaining validation: Terraform plan/apply, actual remote provisioning and server recreation are NOT YET TESTED. No Hetzner API resources were created.

## 7. Monitor the Application

**Assessment: PARTIALLY VALIDATED**

- [x] Implementation documented: Prometheus/Grafana resources, FastAPI metrics, dashboard, ServiceMonitor and unavailable/5xx alert rules.
- [x] Executed checks recorded: All three isolated targets were UP including Grafana; real synthetic request/rate/latency/error metrics rendered; the one-minute unavailable alert fired and cleared after recovery.
- [x] Concrete evidence indexed: [E03: All three Prometheus targets UP](screenshots/07-monitor-the-application/prometheus-targets-up.jpg), [E04: Real request counts, error counts and latency](screenshots/07-monitor-the-application/grafana-request-latency-errors.jpg), [E05: Unavailable alert FIRING after one minute](screenshots/07-monitor-the-application/application-alert-firing.jpg), [E26: Application alert cleared after recovery](screenshots/07-monitor-the-application/E26.jpg), [E27: ServiceMonitor implemented: runtime discovery pending](screenshots/07-monitor-the-application/E27.jpg).
- [ ] Remaining validation: The new ServiceMonitor discovery in Kubernetes, receiver delivery, sustained 5xx alert scenario and durable monitoring recovery are NOT YET TESTED.

## 8. Think About Security (DevSecOps)

Latest: [Alpine security remediation and reproducible checks](backend-security-remediation.md), [E39 scan](screenshots/08-think-about-security-devsecops/E39.jpg), [E40 exact-image integration test](screenshots/08-think-about-security-devsecops/E40.jpg). Historical failures below remain dated evidence.

**Assessment: PARTIALLY VALIDATED**

- [x] Implementation documented: Dependency remediation, strict source/image gates, non-root/read-only controls, dropped capabilities, NetworkPolicies and safe temporary credential cleanup.
- [x] Executed checks recorded: Patched locks including dev dependencies and frontend runtime: 0 HIGH/CRITICAL. Backend progressed from 4 critical/67 high to Debian 0 critical/44 high, then Alpine 0 critical/0 high in the new strict local scan. The rebuilt image passed migrations, login, authenticated CRUD, readiness and metrics with non-root/read-only restrictions. Historical failing hosted evidence is preserved.
- [x] Concrete evidence indexed: [E28: Security before and after remediation](screenshots/08-think-about-security-devsecops/E28.jpg), [E29: Historical Debian security gate fails closed](screenshots/08-think-about-security-devsecops/E29.jpg), [E12: Current source security workflow passes](screenshots/08-think-about-security-devsecops/github-source-security-passed.jpg), [E30: Container security controls configured](screenshots/08-think-about-security-devsecops/E30.jpg), [E31: Default-deny policy and explicit database traffic](screenshots/08-think-about-security-devsecops/E31.jpg), [E32: Temporary credential access removed](screenshots/08-think-about-security-devsecops/E32.jpg).
- [ ] Remaining validation: Fresh hosted CI validation and publication for this change must be checked separately. Live Kubernetes NetworkPolicy enforcement remains NOT YET TESTED; public HTTPS repository access needs no deploy key. The temporary account SSH key was removed.

## 9. Think About Disaster Recovery

**Assessment: PARTIALLY VALIDATED**

- [x] Implementation documented: Atomic compressed PostgreSQL backups, recovery/rollback runbooks and off-node snapshot/token guidance.
- [x] Executed checks recorded: PG16 backup mode 0600, fresh database restore, same browser-created item ID/title, and failed-dump cleanup passed; previous three-row restore also passed.
- [x] Concrete evidence indexed: [E33: Actual backup creation and mode 0600](screenshots/09-think-about-disaster-recovery/E33.jpg), [E34: Restored record matches the browser-created item](screenshots/09-think-about-disaster-recovery/E34.jpg), [E35: Failed backups leave no completed corrupt archive](screenshots/09-think-about-disaster-recovery/E35.jpg), [E07: Browser-created item persists after reload](screenshots/01-dockerize-your-application/item-created-and-persisted.jpg).
- [ ] Remaining validation: GitOps/deployment rollback, actual k3s snapshot/restore, off-site durability and replacement-server recovery are NOT YET TESTED. The kubectl-to-Docker adapter is documented explicitly.

## 10. Documentation

**Assessment: PASSED**

- [x] Implementation documented: Architecture/runbooks, exact ten-heading compliance mapping, provenance-backed screenshot index, capture protocol and both ten-minute plans.
- [x] Executed checks recorded: Screenshot/source hashes, original-image preservation, asset links and offline presentation gallery are checked before delivery.
- [x] Concrete evidence indexed: [E36: Architecture and engineering boundaries](screenshots/10-documentation/E36.jpg).
- [ ] Remaining validation: The architecture is a design view; future cloud boxes are not deployment evidence. This is an evidence pack, not an exported PowerPoint deck.

Use [the mandatory capture protocol](screenshots/capture-protocol.md) in every remaining remediation phase. Record FAILED and NOT YET TESTED explicitly, keep complete text artifacts, and never rerun an expensive stack only to replace already useful evidence.
