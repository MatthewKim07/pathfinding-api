"""Breadth-first search implementation for unweighted grid pathfinding."""

from __future__ import annotations

from collections import deque
from time import perf_counter

import numpy as np
from numpy.typing import NDArray

from app.algorithms.common import (
    GridCoordinate,
    PathfindingResult,
    calculate_path_cost,
    elapsed_ms,
    iter_neighbors,
    reconstruct_path,
    validate_coordinate,
    validate_grid,
)


def run_bfs(
    grid: NDArray[np.int64], start: GridCoordinate, end: GridCoordinate
) -> PathfindingResult:
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
    validate_grid(grid)
    validate_coordinate(grid, start, "start")
    validate_coordinate(grid, end, "end")

    if start == end:
        return PathfindingResult(
            path=[start],
            path_found=True,
            total_cost=0,
            path_length=0,
            visited_nodes=1,
            runtime_ms=elapsed_ms(started_at),
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
            path = reconstruct_path(parents, end)
            return PathfindingResult(
                path=path,
                path_found=True,
                total_cost=calculate_path_cost(grid, path),
                path_length=len(path) - 1,
                visited_nodes=visited_nodes,
                runtime_ms=elapsed_ms(started_at),
            )

        for neighbor in iter_neighbors(grid, current):
            if visited[neighbor]:
                continue

            visited[neighbor] = True
            parents[neighbor] = current
            queue.append(neighbor)

    return PathfindingResult(
        path=[],
        path_found=False,
        total_cost=None,
        path_length=0,
        visited_nodes=visited_nodes,
        runtime_ms=elapsed_ms(started_at),
    )
