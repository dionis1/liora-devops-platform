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
  --version 92.11.0 \
  --values monitoring/kube-prometheus-stack-values.yaml
kubectl -n monitoring get pods
kubectl -n monitoring port-forward service/monitoring-grafana 3000:80
```

Open http://localhost:3000. The chart is pinned to 92.11.0 for local validation; re-render and retest before changing it. Grafana settings and Alertmanager silences are ephemeral with these lab values; configure durable storage and a real alert receiver before deployment. Grafana is deliberately not exposed publicly. Metrics cover node, pods, workloads and Kubernetes health. The reviewed application patch adds internal `/metrics` and a database-backed `/readyz` endpoint.

## Application metrics

Apply the reviewed app patch before building: `bash scripts/prepare-course-app.sh`.
The platform entrypoint imports the original FastAPI app and records bounded route-template
labels with prometheus-client. Request count includes HTTP status; the duration histogram
covers the full response. The public ingress exposes only `/api`, keeping `/metrics` internal.

After installing the chart and its CRDs, run `kubectl apply -k monitoring`.
This installs the backend ServiceMonitor, application-unavailable and sustained 5xx rules,
and the Grafana dashboard ConfigMap. The dashboard uses datasource UID `liora-prometheus`.
NetworkPolicy permits scraping from Prometheus in the monitoring namespace.

The unavailable alert fires after one minute of a failed or absent backend scrape.
Configure an authenticated Alertmanager receiver and test both firing and resolved delivery
before relying on notifications. Alert evaluation alone does not prove notification delivery.
See [second-pass validation](../docs/remediation-report.md) for observed results and limits.
