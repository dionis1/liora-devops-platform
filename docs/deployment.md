# Deferred deployment: from GitHub code to a Hetzner k3s host

**Nothing in this guide has been applied to a host yet.** Do this only when the VM is available. All secrets, Terraform state and kubeconfig must remain outside Git.

## 0. Tools and prerequisites

On your Linux workstation: Terraform >=1.5, Ansible, Git, kubectl, Helm, SSH client, Hetzner API token, an SSH public key, and an available Hetzner server plan. The repository's upstream FastAPI application is stored in `course-app/` as a Git submodule. Use `git clone --recurse-submodules`.

## 1. Terraform (future cloud provisioning)

```bash
cd infrastructure/terraform
cp terraform.tfvars.example terraform.tfvars
# Change ssh_public_key, ssh_allowed_cidrs (your current public /32),
# location and server_type, then save. Do not commit terraform.tfvars.
export HCLOUD_TOKEN="YOUR_TOKEN_FROM_HETZNER"
terraform init
terraform validate
terraform plan -out=plan.tfplan
terraform apply plan.tfplan
cd ../..
bash scripts/create-inventory.sh
```

The default server type is `cx43` but this is only a placeholder until the actual plan is available. Terraform cannot check cloud availability without your account. TCP 22 is accessible only from the trusted CIDRs in your variable file, 80 and 443 are public, and port 6443 is intentionally not public.

**Protect Terraform state:** it contains infrastructure details; `*.tfstate` and `*.tfplan` are excluded from Git. Store encrypted copies outside the repository.

## 2. Bootstrap with Ansible

First verify the Hetzner SSH host key fingerprint independently and accept it. From repository root:

```bash
ansible-playbook -i ansible/inventory/hosts.ini ansible/playbooks/prepare.yml
ansible-playbook -i ansible/inventory/hosts.ini ansible/playbooks/k3s.yml
ansible-playbook -i ansible/inventory/hosts.ini ansible/playbooks/kubeconfig.yml
```

This downloads a local kubeconfig to `.secrets/k3s.yaml`. The kube API is closed in the public firewall. Use an SSH tunnel in a separate terminal (replace HOST_IP):

```bash
ssh -N -L 6443:127.0.0.1:6443 root@HOST_IP
```

On the workstation set `export KUBECONFIG="$PWD/.secrets/k3s.yaml"` and run `kubectl get nodes`. Kubeconfig points to localhost and uses your tunnel.

## 3. Namespace-scoped credentials (never in Git)

Prepare **different** `.secrets/liora-dev.env` and `.secrets/liora-prod.env` files with:

```text
POSTGRES_PASSWORD=<unique long password>
SECRET_KEY=<unique random high-entropy key>
FIRST_SUPERUSER=<unique real admin email>
FIRST_SUPERUSER_PASSWORD=<unique long password>
```

Do not use the example passwords from `course-app/.env` on a publicly reachable service. Execute:

```bash
bash scripts/create-secrets.example.sh liora-dev
bash scripts/create-secrets.example.sh liora-prod
```

For private GHCR images, create a **read:packages** registry token and a `ghcr-pull` docker-registry secret in **both namespaces**. Do not commit the token. The k3s API must be able to pull the SHA-tagged images from GHCR.

## 4. Argo CD and GitOps

```bash
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update
kubectl create namespace argocd --dry-run=client -o yaml | kubectl apply -f -
helm upgrade --install argocd argo/argo-cd -n argocd --wait
```

Use a reviewed chart version for the demonstration (add `--version <version>`); document it. Because the GitHub repository is **private**, configure Argo CD repository access with a read-only GitHub token through the Argo CD UI or an externally managed secret. Never put the token into YAML in this repository.

The `deploy/dev` branch is created by CI after a successful image publish on main. Make sure it exists before applying:

```bash
kubectl apply -f gitops/applications.yaml
kubectl -n argocd get applications
kubectl -n argocd port-forward svc/argocd-server 8080:443
```

Development tracks `deploy/dev` and automatically syncs. Production tracks `main` and requires a manual Argo CD sync.

## 5. Ingress, DNS, HTTPS and image releases

Replace `dev.example.invalid` and `app.example.invalid` in manifests with real DNS names under your control, then point A records to the host IP. They are **deliberately unusable placeholders**. Configure TLS certificates and Traefik TLS ingress before publicly exposing real users; the checked-in manifests are a staging skeleton, **not a secure public production ingress**.

Important: the original React SDK already sends requests starting with `/api/v1`. The frontend Docker build sets `VITE_API_URL` to an empty string; ingress routes `/api` to backend and `/` to frontend. Do not configure `VITE_API_URL=/api`, which would duplicate the prefix.

Both overlays currently have `sha-bootstrap` placeholder image tags. Successful GitHub Actions publish updates **dev** on `deploy/dev`. For **prod**, change the two image tags in `kubernetes/overlays/prod/kustomization.yaml` to the approved SHA, merge to main, and manually sync. Do not try to deploy an unbuilt bootstrap tag.

## 6. Monitoring and backups

See `monitoring/README.md` for Helm installation with limited single-node resources, and `docs/disaster-recovery.md` for PostgreSQL backups, etcd snapshots, restore and image rollback.

## 7. Destroy (after off-host backups)

```bash
cd infrastructure/terraform
terraform destroy
```

Deleting the cloud server deletes local-path volumes. Take backups first. Powered-off Hetzner servers still incur charges.


## Private Git authentication validation

For SSH, add a repository-specific GitHub deploy key with **Allow write access unchecked**.
Verify its fingerprint and that GitHub reports `read_only: true` before installing it.
A key that reads the repo is not proof of read-only scope. Test the exact private key with
`ssh -F /dev/null -i /absolute/private/key -o IdentitiesOnly=yes -o IdentityAgent=none`
so account-level SSH configuration cannot silently provide another identity.

Create the Argo repository Secret locally with the secret-type label `repository`,
`type=git`, `url=git@github.com:dionis1/liora-devops-platform.git`, and `sshPrivateKey`
read from the private file. Do not save the Secret in this repository or print it.
Configure verified GitHub SSH host keys in `argocd-ssh-known-hosts-cm` and use the
matching SSH repoURL in both Applications when choosing SSH authentication.
The checked-in HTTPS URLs instead require a read-only HTTPS credential.
Keep Argo server access on a loopback-only port-forward; remove temporary keys after testing.

The temporary test key could read GitHub, but the repository deploy-key API returned zero keys.
Its scope was therefore not accepted as verified read-only, and it was not installed in Argo.
The exact temporary account-level key was removed with explicit user approval and removal was verified. Dev synchronization, private GHCR pulls, and rollback still require a separate live test.
