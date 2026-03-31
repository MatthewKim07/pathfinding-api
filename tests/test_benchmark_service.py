"""Tests for the benchmark service layer."""

import pandas as pd

from app.schemas import BenchmarkMapInput, BenchmarkRequest, Coordinate
from app.services.benchmark_service import load_latest_benchmark, run_benchmark


def test_run_benchmark_collects_records_and_writes_csv(tmp_path) -> None:
    """Benchmark runs should be persisted and summarized through pandas."""

    request = BenchmarkRequest(
        maps=[
            BenchmarkMapInput(
                name="detour",
                grid=[
                    [1, 9, 1],
                    [1, 9, 1],
                    [1, 1, 1],
                ],
                start=Coordinate(row=0, col=0),
                end=Coordinate(row=0, col=2),
            ),
            BenchmarkMapInput(
                name="blocked",
                grid=[
                    [1, 0],
                    [0, 1],
                ],
                start=Coordinate(row=0, col=0),
                end=Coordinate(row=1, col=1),
            ),
        ],
        algorithms=["bfs", "dijkstra", "astar"],
        repeat_runs=2,
    )

    response = run_benchmark(request, results_dir=tmp_path)

    assert response.total_runs == 12
    assert len(response.records) == 12
    assert len(response.summaries) == 3
    assert all(summary.runs == 4 for summary in response.summaries)
    assert len(response.highlights) == 3
    assert (tmp_path / "latest.csv").exists()
    assert (tmp_path / f"{response.benchmark_id}.csv").exists()

    dataframe = pd.read_csv(tmp_path / "latest.csv")
    assert set(dataframe.columns) == {
        "benchmark_id",
        "algorithm",
        "map_name",
        "rows",
        "cols",
        "repeat",
        "path_found",
        "path_length",
        "total_cost",
        "visited_nodes",
        "runtime_ms",
    }


def test_load_latest_benchmark_returns_saved_summary(tmp_path) -> None:
    """The loader should reconstruct benchmark output from the latest CSV."""

    request = BenchmarkRequest(
        maps=[
            BenchmarkMapInput(
                name="open",
                grid=[
                    [1, 1, 1],
                    [1, 1, 1],
                ],
                start=Coordinate(row=0, col=0),
                end=Coordinate(row=1, col=2),
            )
        ],
        algorithms=["bfs", "dijkstra"],
        repeat_runs=1,
    )

    created = run_benchmark(request, results_dir=tmp_path)
    loaded = load_latest_benchmark(results_dir=tmp_path)

    assert loaded.benchmark_id == created.benchmark_id
    assert loaded.total_runs == created.total_runs
    assert loaded.csv_path.endswith("latest.csv")
    assert [summary.algorithm for summary in loaded.summaries] == ["bfs", "dijkstra"]
