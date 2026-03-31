"""API tests for the pathfinding endpoint."""

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_path_endpoint_runs_bfs_and_returns_the_path_result() -> None:
    """The API should expose the BFS result through the path endpoint."""

    response = client.post(
        "/path",
        json={
            "grid": [
                [1, 4, 0],
                [0, 2, 3],
                [0, 0, 1],
            ],
            "start": {"row": 0, "col": 0},
            "end": {"row": 2, "col": 2},
            "algorithm": "bfs",
        },
    )

    assert response.status_code == 200
    body = response.json()

    assert body["algorithm"] == "bfs"
    assert body["path"] == [
        {"row": 0, "col": 0},
        {"row": 0, "col": 1},
        {"row": 1, "col": 1},
        {"row": 1, "col": 2},
        {"row": 2, "col": 2},
    ]
    assert body["path_found"] is True
    assert body["total_cost"] == 10
    assert body["path_length"] == 4
    assert body["visited_nodes"] == 5
    assert body["runtime_ms"] >= 0


def test_path_endpoint_returns_no_path_for_unreachable_grids() -> None:
    """The API should return a clean no-path response when BFS cannot reach the goal."""

    response = client.post(
        "/path",
        json={
            "grid": [
                [1, 0],
                [0, 1],
            ],
            "start": {"row": 0, "col": 0},
            "end": {"row": 1, "col": 1},
            "algorithm": "bfs",
        },
    )

    assert response.status_code == 200
    body = response.json()

    assert body == {
        "algorithm": "bfs",
        "path": [],
        "path_found": False,
        "total_cost": None,
        "path_length": 0,
        "visited_nodes": 1,
        "runtime_ms": body["runtime_ms"],
    }
    assert body["runtime_ms"] >= 0


def test_path_endpoint_rejects_algorithms_not_implemented_yet() -> None:
    """Only BFS should be available at this milestone."""

    response = client.post(
        "/path",
        json={
            "grid": [
                [1, 1],
                [1, 1],
            ],
            "start": {"row": 0, "col": 0},
            "end": {"row": 1, "col": 1},
            "algorithm": "astar",
        },
    )

    assert response.status_code == 501
    assert response.json() == {
        "detail": "Algorithm 'astar' is not implemented yet."
    }


def test_path_endpoint_returns_422_for_invalid_payloads() -> None:
    """Schema validation errors should surface as FastAPI 422 responses."""

    response = client.post(
        "/path",
        json={
            "grid": [],
            "start": {"row": 0, "col": 0},
            "end": {"row": 0, "col": 0},
            "algorithm": "bfs",
        },
    )

    assert response.status_code == 422
    detail = response.json()["detail"]
    assert any("Grid must contain at least one row." in item["msg"] for item in detail)


def test_path_endpoint_runs_dijkstra_and_returns_the_weighted_optimal_path() -> None:
    """The API should expose Dijkstra's minimum-cost path on weighted grids."""

    response = client.post(
        "/path",
        json={
            "grid": [
                [1, 9, 1],
                [1, 9, 1],
                [1, 1, 1],
            ],
            "start": {"row": 0, "col": 0},
            "end": {"row": 0, "col": 2},
            "algorithm": "dijkstra",
        },
    )

    assert response.status_code == 200
    body = response.json()

    assert body["algorithm"] == "dijkstra"
    assert body["path"] == [
        {"row": 0, "col": 0},
        {"row": 1, "col": 0},
        {"row": 2, "col": 0},
        {"row": 2, "col": 1},
        {"row": 2, "col": 2},
        {"row": 1, "col": 2},
        {"row": 0, "col": 2},
    ]
    assert body["path_found"] is True
    assert body["total_cost"] == 6
    assert body["path_length"] == 6
    assert body["visited_nodes"] > 0
    assert body["runtime_ms"] >= 0
