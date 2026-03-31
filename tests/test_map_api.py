"""API tests for map endpoints."""

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_sample_maps_endpoint_returns_predefined_maps() -> None:
    """The sample maps endpoint should expose the predefined catalog."""

    response = client.get("/maps/sample")

    assert response.status_code == 200
    body = response.json()

    assert "maps" in body
    assert len(body["maps"]) >= 3
    assert all("grid" in sample for sample in body["maps"])
    assert all("start" in sample and "end" in sample for sample in body["maps"])


def test_random_map_endpoint_generates_seeded_maps_reproducibly() -> None:
    """The random map endpoint should reproduce identical maps for the same seed."""

    payload = {
        "rows": 5,
        "cols": 5,
        "obstacle_ratio": 0.3,
        "max_weight": 4,
        "seed": 21,
    }

    first = client.post("/maps/random", json=payload)
    second = client.post("/maps/random", json=payload)

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json() == second.json()


def test_random_map_endpoint_returns_structured_generation_metadata() -> None:
    """The random map endpoint should return the generated grid and metadata."""

    response = client.post(
        "/maps/random",
        json={
            "rows": 4,
            "cols": 6,
            "obstacle_ratio": 0.25,
            "max_weight": 7,
            "seed": 8,
        },
    )

    assert response.status_code == 200
    body = response.json()

    assert len(body["grid"]) == 4
    assert all(len(row) == 6 for row in body["grid"])
    assert body["start"] == {"row": 0, "col": 0}
    assert body["end"] == {"row": 3, "col": 5}
    assert body["guaranteed_path"] is True
    assert all(cell == 0 or 1 <= cell <= 7 for row in body["grid"] for cell in row)
