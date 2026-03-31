"""Smoke tests for the FastAPI application."""

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root_endpoint_returns_service_metadata() -> None:
    """Ensure the root endpoint exposes basic health and service metadata."""

    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "name": "Pathfinding & Route Optimization API",
        "version": "0.1.0",
        "status": "ok",
    }
