# Liora DevOps Platform

**End-to-end DevOps engineering around the existing [DataScientest FastAPI + Traefik project](https://github.com/DataScientest/fastapi-traefik-datascientest-project).** This repo is the course project's infrastructure and delivery layer, not a replacement web application.

> Status: Code-first infrastructure / Kubernetes / GitOps manifests are in development. No live Hetzner deployment has been performed.

## Architecture

See [architecture diagram](docs/architecture.md): GitHub Actions CI tests the DataScientest FastAPI/PostgreSQL/React application, publishes backend/frontend SHA-tagged images to GHCR, updates the dev GitOps branch, and Argo CD reconciles k3s. Terraform provisions the future Hetzner host and firewall; Ansible bootstraps k3s. Prometheus and Grafana monitor the cluster.

## Tech stack

- **Application:** existing DataScientest FastAPI + React + PostgreSQL + Traefik, tracked in `course-app/` as an upstream Git submodule (MIT license).
- **CI:** GitHub Actions with upstream Ruff, pytest/PostgreSQL tests, container builds and GHCR.
- **CD:** Argo CD + Kustomize overlays, dev automatic, prod manual approval.
- **Infrastructure:** Terraform (Hetzner Cloud), Ansible (Ubuntu / pinned k3s).
- **Observability:** kube-prometheus-stack + Grafana, lightweight values for one node.
- **Security/DR:** restricted SSH firewall, GHCR private package credentials, namespace secrets, Trivy scan, etcd/SQL backups and rollback runbooks.

## Clone the real application

```bash
git clone --recurse-submodules https://github.com/dionis1/liora-devops-platform.git
cd liora-devops-platform
git submodule status
```

Already cloned? `git pull --ff-only && git submodule update --init --recursive`.

## Run the upstream app locally

```bash
cd course-app
docker compose build
docker compose up -d --wait backend frontend
```

Try http://localhost:5173 for React and http://localhost:8000/docs for FastAPI. This Compose configuration contains example local credentials. Do not expose it publicly without reconfiguration.

## Repository structure

```text
course-app/                       Upstream application submodule
.github/workflows/ci.yml          Tests, image builds, GHCR, dev promotion
.github/workflows/security.yml    Trivy source and configuration scan
.github/workflows/validate-platform.yml  Static Terraform/Ansible/Kustomize checks
infrastructure/terraform/         Single Hetzner server + firewall + private network
ansible/                           Server preparation and k3s installation
kubernetes/base/                  Backend, frontend, PostgreSQL, Ingress
kubernetes/overlays/dev/          Development namespace and image selection
kubernetes/overlays/prod/         Production namespace and image selection
gitops/applications.yaml          Argo CD applications
monitoring/                       Prometheus and Grafana chart values
scripts/                          Inventory, secret template, SQL backup
docs/                             Architecture, deployment and DR runbooks
```

## Before purchasing a server

Review [deferred deployment runbook](docs/deployment.md). Terraform will **not** execute automatically in CI and neither will Ansible installation. GitHub CI only validates and packages code. Hosted deployments start when you explicitly run the provisioning steps and supply your own credentials and DNS configuration.

## Recovery and limits

See [DR runbook](docs/disaster-recovery.md). One-node k3s is not HA; local PVCs have one failure domain, and no restore drill has been completed. TLS, live alert testing, durable off-site backup automation and hardening are additional gates before claiming real production readiness.
