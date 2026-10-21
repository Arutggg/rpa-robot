import time

import pytest
from fastapi.testclient import TestClient

from app import db
from app.main import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(db, "DB_PATH", tmp_path / "test.db")
    with TestClient(app) as client:
        yield client


def test_status_when_not_running(client):
    response = client.get("/robot/status")
    assert response.status_code == 200
    assert response.json()["running"] is False


def test_start_and_stop(client):
    response = client.post("/robot/start", json={"start_number": 5})
    assert response.status_code == 200
    assert response.json()["running"] is True
    assert response.json()["start_number"] == 5

    response = client.post("/robot/stop")
    assert response.status_code == 200
    assert response.json()["running"] is False


def test_start_without_body_starts_from_zero(client):
    response = client.post("/robot/start")
    assert response.json()["start_number"] == 0


def test_double_start_returns_409(client):
    client.post("/robot/start")
    response = client.post("/robot/start")
    assert response.status_code == 409


def test_stop_when_not_running_returns_409(client):
    response = client.post("/robot/stop")
    assert response.status_code == 409


def test_invalid_start_number_returns_422(client):
    response = client.post("/robot/start", json={"start_number": "abc"})
    assert response.status_code == 422


def test_run_is_saved_to_history(client):
    client.post("/robot/start", json={"start_number": 3})
    time.sleep(1)
    client.post("/robot/stop")

    runs = client.get("/robot/runs").json()
    assert len(runs) == 1
    assert runs[0]["start_number"] == 3
    assert runs[0]["finished_at"] is not None
    assert runs[0]["duration_seconds"] >= 1