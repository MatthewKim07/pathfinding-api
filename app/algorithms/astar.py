"""A* implementation for weighted grid pathfinding."""

from __future__ import annotations

from heapq import heappop, heappush
from itertools import count
from time import perf_counter

import numpy as np
from numpy.typing import NDArray

from app.algorithms.common import (
    GridCoordinate,
    PathfindingResult,
    elapsed_ms,
    iter_neighbors,
    reconstruct_path,
    validate_coordinate,
    validate_grid,
)


def run_astar(
    grid: NDArray[np.int64], start: GridCoordinate, end: GridCoordinate
) -> PathfindingResult:
    """Find the minimum-cost 4-directional path using A* with Manhattan guidance.

    Purpose:
        Prioritize frontier states by `g + h`, where `g` is the cost accumulated
        so far and `h` is the Manhattan distance to the goal. This preserves the
        minimum-cost guarantee while focusing exploration toward the destination.

    Complexity:
        Time is O((rows * cols) log(rows * cols)) in the worst case, matching
        Dijkstra when the heuristic provides little pruning. Space is
        O(rows * cols) for scores, heap state, visited flags, and parents.

    Use cases:
        Prefer A* when the grid is weighted but you want Dijkstra-level optimality
        with goal-directed guidance that often reduces the search space.

    Cost semantics:
        `total_cost` excludes the starting cell and sums only the traversal cost
        of cells entered after leaving the start position.
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

    g_scores = np.full(grid.shape, np.iinfo(np.int64).max, dtype=np.int64)
    visited = np.zeros(grid.shape, dtype=bool)
    parents: dict[GridCoordinate, GridCoordinate | None] = {start: None}
    push_order = count()
    heap: list[tuple[int, int, GridCoordinate]] = [
        (_manhattan_distance(start, end), next(push_order), start)
    ]
    g_scores[start] = 0
    # Count cells that are finalized after being popped with their best-known f-score.
    visited_nodes = 0

    while heap:
        _, _, current = heappop(heap)
        if visited[current]:
            continue

        visited[current] = True
        visited_nodes += 1

        if current == end:
            path = reconstruct_path(parents, end)
            return PathfindingResult(
                path=path,
                path_found=True,
                total_cost=int(g_scores[end]),
                path_length=len(path) - 1,
                visited_nodes=visited_nodes,
                runtime_ms=elapsed_ms(started_at),
            )

        current_cost = int(g_scores[current])
        for neighbor in iter_neighbors(grid, current):
            if visited[neighbor]:
                continue

            tentative_cost = current_cost + int(grid[neighbor])
            if tentative_cost >= int(g_scores[neighbor]):
                continue

            g_scores[neighbor] = tentative_cost
            parents[neighbor] = current
            f_score = tentative_cost + _manhattan_distance(neighbor, end)
            heappush(heap, (f_score, next(push_order), neighbor))

    return PathfindingResult(
        path=[],
        path_found=False,
        total_cost=None,
        path_length=0,
        visited_nodes=visited_nodes,
        runtime_ms=elapsed_ms(started_at),
    )


def _manhattan_distance(a: GridCoordinate, b: GridCoordinate) -> int:
    """Return the Manhattan distance between two grid coordinates."""

    return abs(a[0] - b[0]) + abs(a[1] - b[1])
