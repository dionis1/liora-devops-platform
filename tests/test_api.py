"""FastAPI smoke and behavior tests for the initial CI pipeline."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"service": "taskflow-api", "status": "running"}


def test_liveness() -> None:
    response = client.get("/health/live")
    assert response.status_code == 200
    assert response.json() == {"status": "alive"}


def test_readiness() -> None:
    response = client.get("/health/ready")
    assert response.status_code == 200
    assert response.json() == {"status": "ready"}


def test_create_and_get_task() -> None:
    created = client.post("/tasks", json={"title": "Set up GitHub Actions"})
    assert created.status_code == 201
    task = created.json()
    assert task["title"] == "Set up GitHub Actions"
    assert task["completed"] is False
    assert client.get(f"/tasks/{task['id']}").json() == task
    assert task in client.get("/tasks").json()


def test_empty_title_is_rejected() -> None:
    assert client.post("/tasks", json={"title": ""}).status_code == 422


def test_unknown_task_is_not_found() -> None:
    assert client.get("/tasks/999999").status_code == 404
