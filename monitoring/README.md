# Cluster monitoring (planned installation)

This repo supplies resource-aware values for kube-prometheus-stack. Install only after k3s is running.

Create a Grafana admin Secret in the monitoring namespace locally (never commit credentials).

```bash
kubectl create namespace monitoring --dry-run=client -o yaml | kubectl apply -f -
kubectl -n monitoring create secret generic grafana-admin \
  --from-literal=admin-user=admin \
  --from-literal=admin-password="$(openssl rand -base64 30)"
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm upgrade --install monitoring prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --values monitoring/kube-prometheus-stack-values.yaml
kubectl -n monitoring get pods
kubectl -n monitoring port-forward service/monitoring-grafana 3000:80
```

Open http://localhost:3000. For a reproducible deployment, pin a reviewed Helm chart version using `--version` and document it. Grafana is deliberately not exposed publicly. Metrics cover node, pods, workloads and Kubernetes health. **Upstream FastAPI has no Prometheus /metrics endpoint yet**; API metrics instrumentation is a separate improvement.
