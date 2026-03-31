"""Schemas for benchmark requests and responses."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, StrictInt

from app.schemas.maps import BenchmarkMapInput
from app.schemas.pathfinding import AlgorithmChoice


class BenchmarkRequest(BaseModel):
    """Input payload for multi-map, multi-algorithm benchmark runs."""

    model_config = ConfigDict(extra="forbid")

    maps: list[BenchmarkMapInput] = Field(min_length=1)
    algorithms: list[AlgorithmChoice] = Field(min_length=1)
    repeat_runs: StrictInt = Field(gt=0, le=50)


class BenchmarkRecord(BaseModel):
    """One recorded benchmark execution for a map/algorithm/repeat combination."""

    model_config = ConfigDict(extra="forbid")

    algorithm: AlgorithmChoice
    map_name: str
    rows: int
    cols: int
    repeat: int
    path_found: bool
    path_length: int
    total_cost: int | None
    visited_nodes: int
    runtime_ms: float


class BenchmarkSummary(BaseModel):
    """Human-readable aggregated metrics for one algorithm."""

    model_config = ConfigDict(extra="forbid")

    algorithm: AlgorithmChoice
    runs: int
    avg_runtime_ms: float
    avg_visited_nodes: float
    success_rate: float
    avg_path_length: float | None


class BenchmarkResponse(BaseModel):
    """Structured benchmark output including raw records and comparisons."""

    model_config = ConfigDict(extra="forbid")

    benchmark_id: str
    csv_path: str
    total_runs: int
    summaries: list[BenchmarkSummary]
    highlights: list[str]
    records: list[BenchmarkRecord]
