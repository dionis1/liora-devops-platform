# Local validation screenshots

These are unedited browser screenshots captured on 2026-10-23 from actual local UIs.
The [manifest](manifest.json) records each URL and the scope of the evidence.
The [main README](../../README.md#local-validation-screenshots) embeds the complete gallery.

The monitoring fixture used loopback-only ports and temporary Docker networking,
with memory limits of backend 192 MiB, frontend 64 MiB, Prometheus 192 MiB,
and Grafana 384 MiB. Grafana anonymous Viewer access was enabled only in this
disposable fixture; the platform Helm configuration uses an admin Secret.
The backend had no database in this fixture. Upstream integration tests used a
separate disposable PostgreSQL 16 instance before monitoring started.
Requests and 404s are synthetic validation traffic. No production data or
credentials appear in the images. Application downtime was deliberate.
