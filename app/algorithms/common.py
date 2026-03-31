"""Shared helpers for grid-based pathfinding algorithms."""

from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter

import numpy as np
from numpy.typing import NDArray

GridCoordinate = tuple[int, int]


@dataclass(frozen=True, slots=True)
class PathfindingResult:
    """Normalized result returned by pathfinding algorithms."""

    path: list[GridCoordinate]
    path_found: bool
    total_cost: int | None
    path_length: int
    visited_nodes: int
    runtime_ms: float


def validate_grid(grid: NDArray[np.int64]) -> None:
    """Ensure the internal grid shape and values are valid for traversal."""

    if grid.ndim != 2 or grid.shape[0] == 0 or grid.shape[1] == 0:
        raise ValueError("Grid must be a non-empty 2D array.")
    if np.any(grid < 0):
        raise ValueError("Grid values must be 0 or positive integers.")


def validate_coordinate(
    grid: NDArray[np.int64], coordinate: GridCoordinate, label: str
) -> None:
    """Ensure a coordinate is within bounds and points at a traversable cell."""

    row, col = coordinate
    rows, cols = grid.shape

    if row < 0 or col < 0 or row >= rows or col >= cols:
        raise ValueError(f"{label.capitalize()} coordinate must be within bounds.")
    if grid[row, col] == 0:
        raise ValueError(
            f"{label.capitalize()} coordinate cannot reference a blocked cell."
        )


def iter_neighbors(
    grid: NDArray[np.int64], coordinate: GridCoordinate
) -> tuple[GridCoordinate, ...]:
    """Return traversable neighbors in a deterministic right/down/left/up order."""

    row, col = coordinate
    rows, cols = grid.shape
    neighbors: list[GridCoordinate] = []

    for next_row, next_col in (
        (row, col + 1),
        (row + 1, col),
        (row, col - 1),
        (row - 1, col),
    ):
        if (
            0 <= next_row < rows
            and 0 <= next_col < cols
            and grid[next_row, next_col] > 0
        ):
            neighbors.append((next_row, next_col))

    return tuple(neighbors)


def reconstruct_path(
    parents: dict[GridCoordinate, GridCoordinate | None], end: GridCoordinate
) -> list[GridCoordinate]:
    """Reconstruct the discovered path from the parent map."""

    path: list[GridCoordinate] = []
    current: GridCoordinate | None = end

    while current is not None:
        path.append(current)
        current = parents[current]

    path.reverse()
    return path


def calculate_path_cost(grid: NDArray[np.int64], path: list[GridCoordinate]) -> int:
    """Calculate the cost of a returned path, excluding the starting cell."""

    return int(sum(grid[row, col] for row, col in path[1:]))


def elapsed_ms(started_at: float) -> float:
    """Return elapsed runtime in milliseconds."""

    return (perf_counter() - started_at) * 1000
