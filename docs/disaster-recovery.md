# Disaster recovery runbook

## Current limitations
This one-node k3s lab is **not high availability**. Local-path PVCs and etcd share the VM failure domain. A deleted Hetzner server may lose all data unless backups have been exported off the node. Terraform state must also be backed up securely outside Git.

## PostgreSQL
Before upgrades and at least daily during the demonstration period:
```bash
bash scripts/backup-postgres.sh liora-dev
bash scripts/backup-postgres.sh liora-prod
```
The files land under ignored `.secrets/backups/` on your controller workstation. Encrypt and copy them to an independent backup destination (another disk or remote object storage). A backup only stored on the k3s VM is insufficient. Retain at least several daily snapshots and run a test restore.

Restore is **destructive**; first stop writes to the target database, verify the selected database and backup, and export a current backup. After selecting the right file:
```bash
kubectl -n liora-dev scale deployment/backend --replicas=0
kubectl -n liora-dev exec -i postgres-0 -- pg_restore -U app -d app --exit-on-error --clean --if-exists < .secrets/backups/SELECTED-liora-dev.dump
kubectl -n liora-dev scale deployment/backend --replicas=1
```
Replace the *example filename* with a real backup (without any spaces). Restore into a **fresh temporary database first** before restoring production.

## k3s datastore
Ansible provisions embedded etcd with `--cluster-init` so k3s etcd snapshots can be used:
```bash
sudo k3s etcd-snapshot save --name before-upgrade
sudo k3s etcd-snapshot ls
```
Export the snapshot directory `/var/lib/rancher/k3s/server/db/snapshots/` securely off-host, along with the k3s server token needed for encrypted-data restoration. Never commit tokens or snapshots. Practice a restore on an isolated replacement VM using the [official embedded-etcd restoration procedure](https://docs.k3s.io/cli/etcd-snapshot#restoring-snapshots). Stop k3s, restore the selected snapshot with `--cluster-reset --cluster-reset-restore-path`, then restart without reset flags. Keep the original token available securely; it decrypts bootstrap data ([K3s backup requirements](https://docs.k3s.io/datastore/backup-restore)). These steps were reviewed against the official documentation on 2026-10-23, but no etcd restore was executed in this pass.

## Server failure
1. Record the last available Git SHA, container image digests, database backup timestamps and incident time.
2. Recreate the VM with Terraform from a securely saved state; re-run Ansible k3s setup.
3. Reinstall Argo CD and restore namespace application secrets. Public GitHub/GHCR sources need no repository/registry credential; restore externally managed read-only credentials only when those sources are private.
4. Restore persistent PostgreSQL data from off-host backups; then reconcile the GitOps manifests.
5. Validate health-check endpoint, UI/login, data consistency, Grafana alerts, and backups.

## Rollback
Deployment rollback: revert the production `newTag` values in `kubernetes/overlays/prod/kustomization.yaml` to previously published SHA tags, merge the approved PR and manually re-sync `liora-prod` in Argo CD. For dev, revert the GitOps commit in `deploy/dev` (Argo auto-sync will re-apply). Database migrations are not automatically reversed by image rollback; test migration compatibility and keep a pre-deployment backup.

## Demonstration
Capture screenshots/logs of backup creation, a restored record on a temporary database, and a GitOps rollback. Do not claim these tests passed until executed on a real cluster.


## Local validation evidence

The second pass tested the atomic backup script against disposable PostgreSQL 16.10 with UID/GID 999, a read-only root filesystem, dropped capabilities and temporary writable data/socket directories. A real custom-format dump restored three matching rows into a fresh database. Failed dumps and invalid namespaces produced no completed backup. This exercised the actual script through an explicitly documented kubectl-to-Docker test adapter; it does not prove a cloud PVC or embedded-etcd restore. See [remediation evidence](remediation-evidence/disaster-recovery.txt).

## Verified local GitOps rollback — 2026-10-23

A controlled backend template change and `git revert` were pushed to a separate real GitHub validation branch. Argo auto-sync restored the original template hash and ReplicaSet, reached Synced + Healthy, and the same database item remained accessible. The disposable Application was then returned to `deploy/dev`, verified healthy and removed with its cluster. [Full proof, revisions and limitations](argocd-validation.md). This was a configuration rollback with an unchanged secure image tag; image-version and schema downgrades, k3s snapshots and off-site/cloud recovery remain untested.
