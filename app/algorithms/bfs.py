"""Breadth-first search implementation for unweighted grid pathfinding."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from time import perf_counter

import numpy as np
from numpy.typing import NDArray

GridCoordinate = tuple[int, int]


@dataclass(frozen=True, slots=True)
class BFSResult:
    """Normalized result returned by the BFS search."""

    path: list[GridCoordinate]
    path_found: bool
    total_cost: int | None
    path_length: int
    visited_nodes: int
    runtime_ms: float


def run_bfs(
    grid: NDArray[np.int64], start: GridCoordinate, end: GridCoordinate
) -> BFSResult:
    """Find the shortest 4-directional path on an unweighted grid using BFS.

    Purpose:
        Explore the grid level by level to guarantee the fewest movement steps
        between the start and end coordinates when all moves have equal cost.

    Complexity:
        Time is O(rows * cols) in the worst case because each traversable cell is
        processed at most once. Space is O(rows * cols) for the queue, visited
        state, and parent map.

    Use cases:
        Prefer BFS for unweighted grids or when the primary goal is the minimum
        number of steps rather than the minimum weighted traversal cost.
    """

    started_at = perf_counter()
    _validate_grid(grid)
    _validate_coordinate(grid, start, "start")
    _validate_coordinate(grid, end, "end")

    if start == end:
        return BFSResult(
            path=[start],
            path_found=True,
            total_cost=0,
            path_length=0,
            visited_nodes=1,
            runtime_ms=_elapsed_ms(started_at),
        )

    queue: deque[GridCoordinate] = deque([start])
    visited = np.zeros(grid.shape, dtype=bool)
    visited[start] = True
    parents: dict[GridCoordinate, GridCoordinate | None] = {start: None}
    # Count cells that are actually dequeued and processed by BFS.
    visited_nodes = 0

    while queue:
        current = queue.popleft()
        visited_nodes += 1

        if current == end:
            path = _reconstruct_path(parents, end)
            return BFSResult(
                path=path,
                path_found=True,
                total_cost=_calculate_path_cost(grid, path),
                path_length=len(path) - 1,
                visited_nodes=visited_nodes,
                runtime_ms=_elapsed_ms(started_at),
            )

        for neighbor in _iter_neighbors(grid, current):
            if visited[neighbor]:
                continue

            visited[neighbor] = True
            parents[neighbor] = current
            queue.append(neighbor)

    return BFSResult(
        path=[],
        path_found=False,
        total_cost=None,
        path_length=0,
        visited_nodes=visited_nodes,
        runtime_ms=_elapsed_ms(started_at),
    )


def _validate_grid(grid: NDArray[np.int64]) -> None:
    """Ensure the internal grid shape and values are valid for traversal."""

    if grid.ndim != 2 or grid.shape[0] == 0 or grid.shape[1] == 0:
        raise ValueError("Grid must be a non-empty 2D array.")
    if np.any(grid < 0):
        raise ValueError("Grid values must be 0 or positive integers.")


def _validate_coordinate(
    grid: NDArray[np.int64], coordinate: GridCoordinate, label: str
) -> None:
    """Ensure a coordinate is within bounds and points at a traversable cell."""

    row, col = coordinate
    rows, cols = grid.shape

    if row < 0 or col < 0 or row >= rows or col >= cols:
        raise ValueError(f"{label.capitalize()} coordinate must be within bounds.")
    if grid[row, col] == 0:
        raise ValueError(f"{label.capitalize()} coordinate cannot reference a blocked cell.")


def _iter_neighbors(
    grid: NDArray[np.int64], coordinate: GridCoordinate
) -> tuple[GridCoordinate, ...]:
    """Return traversable neighbors in a deterministic order."""

    row, col = coordinate
    rows, cols = grid.shape
    neighbors: list[GridCoordinate] = []

    for next_row, next_col in (
        (row, col + 1),
        (row + 1, col),
        (row, col - 1),
        (row - 1, col),
    ):
        if 0 <= next_row < rows and 0 <= next_col < cols and grid[next_row, next_col] > 0:
            neighbors.append((next_row, next_col))

    return tuple(neighbors)


def _reconstruct_path(
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


def _calculate_path_cost(
    grid: NDArray[np.int64], path: list[GridCoordinate]
) -> int:
    """Calculate the cost of the returned BFS path, excluding the starting cell.

    BFS still optimizes for the fewest movement steps, not the lowest weighted
    cost. The reported `total_cost` is therefore descriptive for the chosen path
    rather than an optimization target.
    """

    return int(sum(grid[row, col] for row, col in path[1:]))


def _elapsed_ms(started_at: float) -> float:
    """Return elapsed runtime in milliseconds."""

    return (perf_counter() - started_at) * 1000
