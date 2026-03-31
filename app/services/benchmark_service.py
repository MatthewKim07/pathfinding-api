"""Service-layer logic for running and loading benchmark results."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

from app.schemas import (
    BenchmarkRecord,
    BenchmarkRequest,
    BenchmarkResponse,
    BenchmarkSummary,
)
from app.services.path_service import solve_problem

BENCHMARK_RESULTS_DIR = (
    Path(__file__).resolve().parent.parent / "data" / "benchmark_results"
)
LATEST_BENCHMARK_CSV = "latest.csv"


class BenchmarkResultsNotFoundError(FileNotFoundError):
    """Raised when no benchmark CSV is available to load."""


def run_benchmark(
    request: BenchmarkRequest, results_dir: Path | None = None
) -> BenchmarkResponse:
    """Execute benchmark runs, persist raw results to CSV, and return summaries."""

    benchmark_id = datetime.now(UTC).strftime("%Y%m%dT%H%M%S%fZ")
    records: list[dict[str, object]] = []

    for map_index, benchmark_map in enumerate(request.maps, start=1):
        map_name = benchmark_map.name or f"map_{map_index}"
        rows, cols = benchmark_map.shape

        for algorithm in request.algorithms:
            for repeat in range(1, request.repeat_runs + 1):
                result = solve_problem(benchmark_map, algorithm)
                records.append(
                    {
                        "benchmark_id": benchmark_id,
                        "algorithm": algorithm.value,
                        "map_name": map_name,
                        "rows": rows,
                        "cols": cols,
                        "repeat": repeat,
                        "path_found": result.path_found,
                        "path_length": result.path_length,
                        "total_cost": result.total_cost,
                        "visited_nodes": result.visited_nodes,
                        "runtime_ms": result.runtime_ms,
                    }
                )

    dataframe = pd.DataFrame.from_records(records)
    results_path = _write_results_csv(dataframe, benchmark_id, results_dir)
    return _build_benchmark_response(dataframe, benchmark_id, results_path)


def load_latest_benchmark(results_dir: Path | None = None) -> BenchmarkResponse:
    """Load the most recent persisted benchmark results, if available."""

    target_dir = _resolve_results_dir(results_dir)
    latest_path = target_dir / LATEST_BENCHMARK_CSV
    if not latest_path.exists():
        raise BenchmarkResultsNotFoundError("No benchmark results are available yet.")

    dataframe = pd.read_csv(latest_path)
    benchmark_id = str(dataframe["benchmark_id"].iloc[0])
    return _build_benchmark_response(dataframe, benchmark_id, latest_path)


def _write_results_csv(
    dataframe: pd.DataFrame, benchmark_id: str, results_dir: Path | None
) -> Path:
    """Persist benchmark results to a timestamped CSV and update latest.csv."""

    target_dir = _resolve_results_dir(results_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    archived_path = target_dir / f"{benchmark_id}.csv"
    latest_path = target_dir / LATEST_BENCHMARK_CSV
    dataframe.to_csv(archived_path, index=False)
    dataframe.to_csv(latest_path, index=False)
    return archived_path


def _resolve_results_dir(results_dir: Path | None) -> Path:
    """Resolve the directory used for benchmark CSV persistence."""

    return Path(results_dir) if results_dir is not None else BENCHMARK_RESULTS_DIR


def _build_benchmark_response(
    dataframe: pd.DataFrame, benchmark_id: str, csv_path: Path
) -> BenchmarkResponse:
    """Convert a benchmark DataFrame into the structured API response."""

    summaries = _build_summaries(dataframe)
    return BenchmarkResponse(
        benchmark_id=benchmark_id,
        csv_path=str(csv_path),
        total_runs=int(len(dataframe)),
        summaries=summaries,
        highlights=_build_highlights(summaries),
        records=_build_records(dataframe),
    )


def _build_summaries(dataframe: pd.DataFrame) -> list[BenchmarkSummary]:
    """Aggregate per-algorithm statistics for a human-readable benchmark summary."""

    summaries: list[BenchmarkSummary] = []
    grouped = dataframe.groupby("algorithm", sort=True)

    for algorithm, group in grouped:
        successful_runs = group[group["path_found"]]
        avg_path_length = (
            float(successful_runs["path_length"].mean())
            if not successful_runs.empty
            else None
        )
        summaries.append(
            BenchmarkSummary(
                algorithm=algorithm,
                runs=int(len(group)),
                avg_runtime_ms=float(group["runtime_ms"].mean()),
                avg_visited_nodes=float(group["visited_nodes"].mean()),
                success_rate=float(group["path_found"].mean() * 100),
                avg_path_length=avg_path_length,
            )
        )

    return summaries


def _build_highlights(summaries: list[BenchmarkSummary]) -> list[str]:
    """Create short benchmark comparisons that are easier to scan than raw metrics."""

    if not summaries:
        return []

    fastest = min(summaries, key=lambda summary: summary.avg_runtime_ms)
    least_visited = min(summaries, key=lambda summary: summary.avg_visited_nodes)
    highest_success = max(summaries, key=lambda summary: summary.success_rate)

    return [
        (
            f"Fastest average runtime: {fastest.algorithm.value} "
            f"at {fastest.avg_runtime_ms:.3f} ms."
        ),
        (
            f"Fewest average visited nodes: {least_visited.algorithm.value} "
            f"at {least_visited.avg_visited_nodes:.1f}."
        ),
        (
            f"Highest success rate: {highest_success.algorithm.value} "
            f"at {highest_success.success_rate:.1f}%."
        ),
    ]


def _build_records(dataframe: pd.DataFrame) -> list[BenchmarkRecord]:
    """Convert raw benchmark rows into typed response records."""

    records: list[BenchmarkRecord] = []

    for row in dataframe.to_dict(orient="records"):
        total_cost = row["total_cost"]
        records.append(
            BenchmarkRecord(
                algorithm=row["algorithm"],
                map_name=str(row["map_name"]),
                rows=int(row["rows"]),
                cols=int(row["cols"]),
                repeat=int(row["repeat"]),
                path_found=bool(row["path_found"]),
                path_length=int(row["path_length"]),
                total_cost=None if pd.isna(total_cost) else int(total_cost),
                visited_nodes=int(row["visited_nodes"]),
                runtime_ms=float(row["runtime_ms"]),
            )
        )

    return records
