"""Tests for the health and readiness endpoints."""

from __future__ import annotations

from fastapi.testclient import TestClient

from llamaindex_rag.main import create_app


def test_health_returns_200() -> None:
    """The /health endpoint should return 200 with an 'ok' status."""

    client = TestClient(create_app())
    response = client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["service"]
    assert body["version"]


def test_ready_returns_200() -> None:
    """The /ready endpoint should return 200 and a status field."""

    client = TestClient(create_app())
    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json()["status"] in {"ready", "pending"}
