# Final compliance report

Assessment date: 2026-10-23. Functional/configuration revision: **211199d**; later evidence-only commits do not turn these dated workflow records into new release results. The repository is now public. No cloud resources were provisioned.

**Evidence coverage: 10/10 requirements. Assessment: 3 PASSED, 7 PARTIALLY VALIDATED, 0 FAILED. This is not 10/10 end-to-end deployment success. Public production readiness: NO.**

| Official requirement | Assessment | Best evidence |
| --- | --- | --- |
| 1. Dockerize Your Application | PASSED | [E07: Browser-created item persists after reload](screenshots/01-dockerize-your-application/item-created-and-persisted.jpg), [E08: Executed Swagger request returns HTTP 200](screenshots/01-dockerize-your-application/swagger-real-health-200.jpg) |
| 2. Deploy the Application in Multiple Environments (Dev & Prod) | PARTIALLY VALIDATED | [E19: Dev and prod separation: static manifests](screenshots/02-deploy-the-application-in-multiple-environments-dev-prod/E19.jpg), [E20: Historical dev pods and Services READY](screenshots/04-container-orchestration-with-kubernetes/E20.jpg) |
| 3. Run Tests on the Application | PASSED | [E16: 55 upstream tests passed](screenshots/03-run-tests-on-the-application/E16.jpg), [E17: Platform metrics and readiness tests passed](screenshots/03-run-tests-on-the-application/E17.jpg) |
| 4. Container Orchestration with Kubernetes | PARTIALLY VALIDATED | [E20: Historical dev pods and Services READY](screenshots/04-container-orchestration-with-kubernetes/E20.jpg), [E21: Historical PVC and Kubernetes HTTP access](screenshots/04-container-orchestration-with-kubernetes/E21.jpg) |
| 5. Automate Deployment (CI/CD Pipeline) | PARTIALLY VALIDATED | [E09: Historical Debian CI blocks publication](screenshots/05-automate-deployment-ci-cd-pipeline/github-current-security-gate.jpg), [E10: Historical successful GHCR publication and dev promotion](screenshots/05-automate-deployment-ci-cd-pipeline/github-historical-publish-promote.jpg) |
| 6. Create IaC (Infrastructure as Code) Templates | PARTIALLY VALIDATED | [E24: Terraform formatting and validation passed](screenshots/06-create-iac-infrastructure-as-code-templates/E24.jpg), [E25: Three Ansible syntax checks passed](screenshots/06-create-iac-infrastructure-as-code-templates/E25.jpg) |
| 7. Monitor the Application | PARTIALLY VALIDATED | [E03: All three Prometheus targets UP](screenshots/07-monitor-the-application/prometheus-targets-up.jpg), [E04: Real request counts, error counts and latency](screenshots/07-monitor-the-application/grafana-request-latency-errors.jpg) |
| 8. Think About Security (DevSecOps) | PARTIALLY VALIDATED | [E28: Security before and after remediation](screenshots/08-think-about-security-devsecops/E28.jpg), [E29: Historical Debian security gate fails closed](screenshots/08-think-about-security-devsecops/E29.jpg) |
| 9. Think About Disaster Recovery | PARTIALLY VALIDATED | [E33: Actual backup creation and mode 0600](screenshots/09-think-about-disaster-recovery/E33.jpg), [E34: Restored record matches the browser-created item](screenshots/09-think-about-disaster-recovery/E34.jpg) |
| 10. Documentation | PASSED | [E36: Architecture and engineering boundaries](screenshots/10-documentation/E36.jpg) |

## 1. Dockerize Your Application

**Assessment: PASSED**

**Implemented:** Multi-stage, non-root platform images around the original pinned DataScientest application; digest-pinned Alpine backend, health checks and a reviewed dependency patch.

**Tested:** Sequential builds, actual API/database readiness, authenticated browser login, item creation and persistence after reload in a Docker fixture with a temporary same-origin Nginx API proxy. Historical main publication succeeded.

**Evidence:** [E07: Browser-created item persists after reload](screenshots/01-dockerize-your-application/item-created-and-persisted.jpg), [E08: Executed Swagger request returns HTTP 200](screenshots/01-dockerize-your-application/swagger-real-health-200.jpg), [E13: Backend image build completed](screenshots/01-dockerize-your-application/E13.jpg), [E14: Frontend TypeScript and production bundle completed](screenshots/01-dockerize-your-application/E14.jpg), [E15: Running containers and health checks](screenshots/01-dockerize-your-application/E15.jpg), [E10: Historical successful GHCR publication and dev promotion](screenshots/05-automate-deployment-ci-cd-pipeline/github-historical-publish-promote.jpg).

**FAILED / NOT YET TESTED:** Publication and authenticated registry pulls for the new Alpine backend are NOT YET TESTED. PR checks do not publish; publication/promotion require a validated push to main. Historical publication evidence is retained.

## 2. Deploy the Application in Multiple Environments (Dev & Prod)

**Assessment: PARTIALLY VALIDATED**

**Implemented:** Separate dev/prod namespaces, overlays, host settings, credentials references and a production TLS Secret reference.

**Tested:** Both overlays render; first-pass dev deployment and routing ran locally.

**Evidence:** [E19: Dev and prod separation: static manifests](screenshots/02-deploy-the-application-in-multiple-environments-dev-prod/E19.jpg), [E20: Historical dev pods and Services READY](screenshots/04-container-orchestration-with-kubernetes/E20.jpg), [E21: Historical PVC and Kubernetes HTTP access](screenshots/04-container-orchestration-with-kubernetes/E21.jpg).

**FAILED / NOT YET TESTED:** Production deployment and public TLS are NOT YET TESTED; final hardened dev manifests were not redeployed.

## 3. Run Tests on the Application

**Assessment: PASSED**

**Implemented:** Upstream tests, PostgreSQL migrations, mypy/Ruff, and metrics/readiness checks run in CI.

**Tested:** 55 upstream tests and 2 platform tests pass; exact CI script passes locally and hosted backend-tests/lint jobs passed at 211199d. New browser login/create/reload smoke passed.

**Evidence:** [E16: 55 upstream tests passed](screenshots/03-run-tests-on-the-application/E16.jpg), [E17: Platform metrics and readiness tests passed](screenshots/03-run-tests-on-the-application/E17.jpg), [E18: Mypy and Ruff passed](screenshots/03-run-tests-on-the-application/E18.jpg), [E09: Historical Debian CI blocks publication](screenshots/05-automate-deployment-ci-cd-pipeline/github-current-security-gate.jpg), [E07: Browser-created item persists after reload](screenshots/01-dockerize-your-application/item-created-and-persisted.jpg).

**FAILED / NOT YET TESTED:** The complete automated browser E2E suite and OpenAPI-client regeneration are NOT YET TESTED.

## 4. Container Orchestration with Kubernetes

**Assessment: PARTIALLY VALIDATED**

**Implemented:** Deployments, StatefulSet, PVC, Services, ConfigMap, Ingress, namespace policy and resource/security settings.

**Tested:** Historical local dev pods reached 1/1 Ready, PVC Bound, rollouts completed, and frontend/backend/Traefik HTTP routing passed; new manifests render.

**Evidence:** [E20: Historical dev pods and Services READY](screenshots/04-container-orchestration-with-kubernetes/E20.jpg), [E21: Historical PVC and Kubernetes HTTP access](screenshots/04-container-orchestration-with-kubernetes/E21.jpg), [E37: Historical ConfigMap, Ingress and rollout results](screenshots/04-container-orchestration-with-kubernetes/E37.jpg), [E19: Dev and prod separation: static manifests](screenshots/02-deploy-the-application-in-multiple-environments-dev-prod/E19.jpg).

**FAILED / NOT YET TESTED:** Historical cluster was deleted. Current hardened cluster, policy enforcement, node-readiness screenshot and cloud deployment are NOT YET TESTED.

## 5. Automate Deployment (CI/CD Pipeline)

**Assessment: PARTIALLY VALIDATED**

**Implemented:** Tests/build/scan gates, exact-scanned-image publication, dev manifest promotion and manual production sync policy; Argo Application manifests.

**Tested:** Historical main publication/promotion passed. Debian at 211199d failed with 44 HIGH findings. The Alpine fix at 34bf33e passed hosted CI: backend tests/lint, platform validation, exact-image PostgreSQL integration, and both strict image scans. Source security audit also passed. PR publication/promotion intentionally skip; historical Argo comparison failed.

**Evidence:** [E09: Historical Debian CI blocks publication](screenshots/05-automate-deployment-ci-cd-pipeline/github-current-security-gate.jpg), [E10: Historical successful GHCR publication and dev promotion](screenshots/05-automate-deployment-ci-cd-pipeline/github-historical-publish-promote.jpg), [E22: Argo CD ran, but private repository comparison failed](screenshots/05-automate-deployment-ci-cd-pipeline/E22.jpg), [E23: Production manual sync configuration](screenshots/05-automate-deployment-ci-cd-pipeline/E23.jpg), [E38: Historical Argo components ready; sync still unproven](screenshots/05-automate-deployment-ci-cd-pipeline/E38.jpg).

**FAILED / NOT YET TESTED:** Successful Argo Synced/Healthy application, public-repo reconciliation and rollback are NOT YET TESTED. The repository became public on 2026-10-23; historical private auth errors do not establish a current public auth failure.

## 6. Create IaC (Infrastructure as Code) Templates

**Assessment: PARTIALLY VALIDATED**

**Implemented:** Terraform Hetzner templates and Ansible preparation/k3s/kubeconfig playbooks, with restricted SSH configuration.

**Tested:** Fresh Terraform fmt/validate and three Ansible syntax checks passed; hosted platform validation passed.

**Evidence:** [E24: Terraform formatting and validation passed](screenshots/06-create-iac-infrastructure-as-code-templates/E24.jpg), [E25: Three Ansible syntax checks passed](screenshots/06-create-iac-infrastructure-as-code-templates/E25.jpg), [E11: Current Terraform, Ansible and Kustomize workflow passes](screenshots/06-create-iac-infrastructure-as-code-templates/github-platform-validation-passed.jpg).

**FAILED / NOT YET TESTED:** Terraform plan/apply, actual remote provisioning and server recreation are NOT YET TESTED. No Hetzner API resources were created.

## 7. Monitor the Application

**Assessment: PARTIALLY VALIDATED**

**Implemented:** Prometheus/Grafana resources, FastAPI metrics, dashboard, ServiceMonitor and unavailable/5xx alert rules.

**Tested:** All three isolated targets were UP including Grafana; real synthetic request/rate/latency/error metrics rendered; the one-minute unavailable alert fired and cleared after recovery.

**Evidence:** [E03: All three Prometheus targets UP](screenshots/07-monitor-the-application/prometheus-targets-up.jpg), [E04: Real request counts, error counts and latency](screenshots/07-monitor-the-application/grafana-request-latency-errors.jpg), [E05: Unavailable alert FIRING after one minute](screenshots/07-monitor-the-application/application-alert-firing.jpg), [E26: Application alert cleared after recovery](screenshots/07-monitor-the-application/E26.jpg), [E27: ServiceMonitor implemented: runtime discovery pending](screenshots/07-monitor-the-application/E27.jpg).

**FAILED / NOT YET TESTED:** The new ServiceMonitor discovery in Kubernetes, receiver delivery, sustained 5xx alert scenario and durable monitoring recovery are NOT YET TESTED.

## 8. Think About Security (DevSecOps)

Hosted proof: [E41 passing image gate](screenshots/08-think-about-security-devsecops/E41.jpg) and [E42 complete CI success](screenshots/05-automate-deployment-ci-cd-pipeline/E42.jpg), both at `34bf33e`.

Latest: [Alpine security remediation and reproducible checks](backend-security-remediation.md), [E39 scan](screenshots/08-think-about-security-devsecops/E39.jpg), [E40 exact-image integration test](screenshots/08-think-about-security-devsecops/E40.jpg). Historical failures below remain dated evidence.

**Assessment: PARTIALLY VALIDATED**

**Implemented:** Dependency remediation, strict source/image gates, non-root/read-only controls, dropped capabilities, NetworkPolicies and safe temporary credential cleanup.

**Tested:** Backend progressed from 4 critical/67 high to Debian 0 critical/44 high, then Alpine 0 critical/0 high locally. At 34bf33e, hosted source security and both strict image scans passed. The exact Alpine image passed migrations, login/JWT, authenticated CRUD, health/readiness and metrics under non-root/read-only restrictions. Historical failures are preserved.

**Evidence:** [E28: Security before and after remediation](screenshots/08-think-about-security-devsecops/E28.jpg), [E29: Historical Debian security gate fails closed](screenshots/08-think-about-security-devsecops/E29.jpg), [E12: Current source security workflow passes](screenshots/08-think-about-security-devsecops/github-source-security-passed.jpg), [E30: Container security controls configured](screenshots/08-think-about-security-devsecops/E30.jpg), [E31: Default-deny policy and explicit database traffic](screenshots/08-think-about-security-devsecops/E31.jpg), [E32: Temporary credential access removed](screenshots/08-think-about-security-devsecops/E32.jpg).

**FAILED / NOT YET TESTED:** Publication for the Alpine fix is NOT YET TESTED; CI publishes only on a validated main push. Live Kubernetes NetworkPolicy enforcement remains NOT YET TESTED; public HTTPS repository access needs no deploy key. The temporary account SSH key was removed.

## 9. Think About Disaster Recovery

**Assessment: PARTIALLY VALIDATED**

**Implemented:** Atomic compressed PostgreSQL backups, recovery/rollback runbooks and off-node snapshot/token guidance.

**Tested:** PG16 backup mode 0600, fresh database restore, same browser-created item ID/title, and failed-dump cleanup passed; previous three-row restore also passed.

**Evidence:** [E33: Actual backup creation and mode 0600](screenshots/09-think-about-disaster-recovery/E33.jpg), [E34: Restored record matches the browser-created item](screenshots/09-think-about-disaster-recovery/E34.jpg), [E35: Failed backups leave no completed corrupt archive](screenshots/09-think-about-disaster-recovery/E35.jpg), [E07: Browser-created item persists after reload](screenshots/01-dockerize-your-application/item-created-and-persisted.jpg).

**FAILED / NOT YET TESTED:** GitOps/deployment rollback, actual k3s snapshot/restore, off-site durability and replacement-server recovery are NOT YET TESTED. The kubectl-to-Docker adapter is documented explicitly.

## 10. Documentation

**Assessment: PASSED**

**Implemented:** Architecture/runbooks, exact ten-heading compliance mapping, provenance-backed screenshot index, capture protocol and both ten-minute plans.

**Tested:** Screenshot/source hashes, original-image preservation, asset links and offline presentation gallery are checked before delivery.

**Evidence:** [E36: Architecture and engineering boundaries](screenshots/10-documentation/E36.jpg).

**FAILED / NOT YET TESTED:** The architecture is a design view; future cloud boxes are not deployment evidence. This is an evidence pack, not an exported PowerPoint deck.

The failing backend security gate must remain enabled. Historical publication and local Kubernetes evidence are dated separately from the current remediation snapshot. Read the [evidence index](screenshots/README.md), [missing-evidence register](presentation-evidence/missing-evidence.md), and [presentation plans](presentation-evidence.md).
