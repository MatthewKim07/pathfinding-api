"""Dijkstra implementation for weighted grid pathfinding."""

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


def run_dijkstra(
    grid: NDArray[np.int64], start: GridCoordinate, end: GridCoordinate
) -> PathfindingResult:
    """Find the minimum-cost 4-directional path on a weighted grid.

    Purpose:
        Explore the frontier in ascending total-cost order so the first time a
        node is finalized, the cheapest path to it has been found.

    Complexity:
        Time is O((rows * cols) log(rows * cols)) in the worst case because heap
        operations dominate frontier updates. Space is O(rows * cols) for the
        heap, distance table, visited state, and parent map.

    Use cases:
        Prefer Dijkstra when grid weights matter and the optimal route should be
        chosen by total traversal cost rather than the fewest number of steps.
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

    distances = np.full(grid.shape, np.iinfo(np.int64).max, dtype=np.int64)
    visited = np.zeros(grid.shape, dtype=bool)
    parents: dict[GridCoordinate, GridCoordinate | None] = {start: None}
    push_order = count()
    heap: list[tuple[int, int, GridCoordinate]] = [(0, next(push_order), start)]
    distances[start] = 0
    # Count cells that are finalized after being popped with their best-known cost.
    visited_nodes = 0

    while heap:
        current_cost, _, current = heappop(heap)
        if visited[current]:
            continue

        visited[current] = True
        visited_nodes += 1

        if current == end:
            path = reconstruct_path(parents, end)
            return PathfindingResult(
                path=path,
                path_found=True,
                total_cost=int(current_cost),
                path_length=len(path) - 1,
                visited_nodes=visited_nodes,
                runtime_ms=elapsed_ms(started_at),
            )

        for neighbor in iter_neighbors(grid, current):
            if visited[neighbor]:
                continue

            next_cost = current_cost + int(grid[neighbor])
            if next_cost >= int(distances[neighbor]):
                continue

            distances[neighbor] = next_cost
            parents[neighbor] = current
            heappush(heap, (next_cost, next(push_order), neighbor))

    return PathfindingResult(
        path=[],
        path_found=False,
        total_cost=None,
        path_length=0,
        visited_nodes=visited_nodes,
        runtime_ms=elapsed_ms(started_at),
    )
