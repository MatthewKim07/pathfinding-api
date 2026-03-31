"""API tests for benchmark endpoints."""

from fastapi.testclient import TestClient

from app.main import app
from app.services import benchmark_service


client = TestClient(app)


def test_benchmark_endpoint_runs_and_returns_summary(monkeypatch, tmp_path) -> None:
    """The benchmark endpoint should execute runs and return aggregated comparisons."""

    monkeypatch.setattr(benchmark_service, "BENCHMARK_RESULTS_DIR", tmp_path)

    response = client.post(
        "/benchmark",
        json={
            "maps": [
                {
                    "name": "detour",
                    "grid": [
                        [1, 9, 1],
                        [1, 9, 1],
                        [1, 1, 1],
                    ],
                    "start": {"row": 0, "col": 0},
                    "end": {"row": 0, "col": 2},
                },
                {
                    "name": "blocked",
                    "grid": [
                        [1, 0],
                        [0, 1],
                    ],
                    "start": {"row": 0, "col": 0},
                    "end": {"row": 1, "col": 1},
                },
            ],
            "algorithms": ["bfs", "dijkstra", "astar"],
            "repeat_runs": 2,
        },
    )

    assert response.status_code == 200
    body = response.json()

    assert body["total_runs"] == 12
    assert len(body["summaries"]) == 3
    assert len(body["highlights"]) == 3
    assert len(body["records"]) == 12
    assert any(summary["algorithm"] == "astar" for summary in body["summaries"])
    assert (tmp_path / "latest.csv").exists()


def test_benchmark_sample_endpoint_returns_latest_results(monkeypatch, tmp_path) -> None:
    """The sample benchmark endpoint should return the most recently saved benchmark."""

    monkeypatch.setattr(benchmark_service, "BENCHMARK_RESULTS_DIR", tmp_path)

    client.post(
        "/benchmark",
        json={
            "maps": [
                {
                    "name": "open",
                    "grid": [
                        [1, 1, 1],
                        [1, 1, 1],
                    ],
                    "start": {"row": 0, "col": 0},
                    "end": {"row": 1, "col": 2},
                }
            ],
            "algorithms": ["bfs", "dijkstra"],
            "repeat_runs": 1,
        },
    )

    response = client.get("/benchmark/sample")

    assert response.status_code == 200
    body = response.json()

    assert body["total_runs"] == 2
    assert body["csv_path"].endswith("latest.csv")
    assert [summary["algorithm"] for summary in body["summaries"]] == [
        "bfs",
        "dijkstra",
    ]
