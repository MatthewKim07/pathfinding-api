"""Unit tests for the A* pathfinding implementation."""

import numpy as np

from app.algorithms import run_astar, run_dijkstra


def test_run_astar_returns_the_minimum_cost_path_on_a_weighted_grid() -> None:
    """A* should find the optimal weighted path, not just a heuristic guess."""

    grid = np.array(
        [
            [1, 5, 1],
            [1, 1, 1],
            [9, 9, 1],
        ],
        dtype=np.int64,
    )

    result = run_astar(grid=grid, start=(0, 0), end=(0, 2))

    assert result.path_found is True
    assert result.path == [(0, 0), (1, 0), (1, 1), (1, 2), (0, 2)]
    assert result.total_cost == 4
    assert result.path_length == 4
    assert result.visited_nodes > 0
    assert result.runtime_ms >= 0


def test_run_astar_matches_dijkstra_on_weighted_optimality() -> None:
    """A* should return the same optimal path cost as Dijkstra on weighted grids."""

    grid = np.array(
        [
            [1, 9, 1],
            [1, 9, 1],
            [1, 1, 1],
        ],
        dtype=np.int64,
    )

    astar_result = run_astar(grid=grid, start=(0, 0), end=(0, 2))
    dijkstra_result = run_dijkstra(grid=grid, start=(0, 0), end=(0, 2))

    assert astar_result.path_found is True
    assert astar_result.path == dijkstra_result.path
    assert astar_result.total_cost == dijkstra_result.total_cost == 6
    assert astar_result.path_length == dijkstra_result.path_length == 6
    assert astar_result.runtime_ms >= 0


def test_run_astar_handles_stale_entries_and_start_end_edge_cases() -> None:
    """A* should handle both the trivial and stale-entry scenarios cleanly."""

    trivial_grid = np.array(
        [
            [3, 1],
            [1, 1],
        ],
        dtype=np.int64,
    )
    trivial_result = run_astar(grid=trivial_grid, start=(0, 0), end=(0, 0))

    assert trivial_result.path_found is True
    assert trivial_result.path == [(0, 0)]
    assert trivial_result.total_cost == 0
    assert trivial_result.path_length == 0
    assert trivial_result.visited_nodes == 1

    stale_grid = np.array(
        [
            [1, 1, 50, 1],
            [1, 1, 1, 1],
        ],
        dtype=np.int64,
    )
    stale_result = run_astar(grid=stale_grid, start=(0, 0), end=(0, 3))

    assert stale_result.path_found is True
    assert stale_result.path == [(0, 0), (0, 1), (1, 1), (1, 2), (1, 3), (0, 3)]
    assert stale_result.total_cost == 5
    assert stale_result.path_length == 5
    assert stale_result.runtime_ms >= 0


def test_run_astar_returns_no_path_when_destination_is_unreachable() -> None:
    """A* should fail cleanly when no route exists."""

    grid = np.array(
        [
            [1, 0],
            [0, 1],
        ],
        dtype=np.int64,
    )

    result = run_astar(grid=grid, start=(0, 0), end=(1, 1))

    assert result.path_found is False
    assert result.path == []
    assert result.total_cost is None
    assert result.path_length == 0
    assert result.visited_nodes == 1
    assert result.runtime_ms >= 0
