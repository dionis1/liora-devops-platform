"""Exercise the real platform entrypoint without a database or a second app."""

from fastapi.testclient import TestClient
from prometheus_client.parser import text_string_to_metric_families

from app.platform_metrics import app


def test_request_error_and_duration_metrics() -> None:
    def fail_for_test() -> None:
        raise RuntimeError("deliberate metrics test failure")

    # This route exists only in this test process and is never in the image.
    app.add_api_route("/__metrics_test_error", fail_for_test, tags=["platform-tests"])
    with TestClient(app, raise_server_exceptions=False) as client:
        assert client.get("/api/v1/utils/health-check/").status_code == 200
        assert client.get("/__metrics_test_error").status_code == 500
        response = client.get("/metrics")
        assert response.status_code == 200
        samples = [
            sample
            for family in text_string_to_metric_families(response.text)
            for sample in family.samples
        ]
        counts = [sample for sample in samples if sample.name == "http_requests_total"]
        assert any(sample.labels.get("status") == "200" for sample in counts)
        assert any(sample.labels.get("status") == "500" for sample in counts)
        assert any(sample.name == "http_request_duration_seconds_count" for sample in samples)
        assert "/metrics" not in client.get("/api/v1/openapi.json").json()["paths"]


def test_readiness_fails_closed_when_database_unavailable(monkeypatch) -> None:
    import psycopg
    import app.platform_metrics as metrics

    def unavailable(**kwargs):
        assert kwargs["connect_timeout"] == 2
        raise psycopg.OperationalError("test-only connection failure")

    monkeypatch.setattr(metrics.psycopg, "connect", unavailable)
    with TestClient(app) as client:
        response = client.get("/readyz")
        assert response.status_code == 503
        assert response.text == "database unavailable"
        assert "test-only" not in response.text
