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
kubectl -n liora-dev exec -i postgres-0 -- pg_restore -U app -d app --clean --if-exists < .secrets/backups/SELECTED-l iora-dev.dump
kubectl -n liora-dev scale deployment/backend --replicas=1
```
Replace the *example filename* with a real backup (without any spaces). Restore into a **fresh temporary database first** before restoring production.

## k3s datastore
Ansible provisions embedded etcd with `--cluster-init` so k3s etcd snapshots can be used:
```bash
sudo k3s etcd-snapshot save --name before-upgrade
sudo k3s etcd-snapshot ls
```
Export the snapshot directory `/var/lib/rancher/k3s/server/db/snapshots/` securely off-host, along with the k3s server token needed for encrypted-data restoration. Never commit tokens or snapshots. Practice a documented restore on an isolated replacement VM using the current official k3s snapshot restoration procedure.

## Server failure
1. Record the last available Git SHA, container image digests, database backup timestamps and incident time.
2. Recreate the VM with Terraform from a securely saved state; re-run Ansible k3s setup.
3. Reinstall Argo CD, restore its private Git repository credentials and namespace secrets.
4. Restore persistent PostgreSQL data from off-host backups; then reconcile the GitOps manifests.
5. Validate health-check endpoint, UI/login, data consistency, Grafana alerts, and backups.

## Rollback
Deployment rollback: revert the production `newTag` values in `kubernetes/overlays/prod/kustomization.yaml` to previously published SHA tags, merge the approved PR and manually re-sync `liora-prod` in Argo CD. For dev, revert the GitOps commit in `deploy/dev` (Argo auto-sync will re-apply). Database migrations are not automatically reversed by image rollback; test migration compatibility and keep a pre-deployment backup.

## Demonstration
Capture screenshots/logs of backup creation, a restored record on a temporary database, and a GitOps rollback. Do not claim these tests passed until executed on a real cluster.
