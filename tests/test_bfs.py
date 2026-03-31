"""Unit tests for the BFS pathfinding implementation."""

import numpy as np

from app.algorithms import run_bfs


def test_run_bfs_reconstructs_the_expected_shortest_path() -> None:
    """BFS should return the shortest step-count path on a small grid."""

    grid = np.array(
        [
            [1, 4, 0],
            [0, 2, 3],
            [0, 0, 1],
        ],
        dtype=np.int64,
    )

    result = run_bfs(grid=grid, start=(0, 0), end=(2, 2))

    assert result.path_found is True
    assert result.path == [(0, 0), (0, 1), (1, 1), (1, 2), (2, 2)]
    assert result.total_cost == 10
    assert result.path_length == 4
    assert result.visited_nodes == 5
    assert result.runtime_ms >= 0


def test_run_bfs_uses_deterministic_neighbor_order_for_tied_paths() -> None:
    """BFS should prefer the right-first route when multiple shortest paths exist."""

    grid = np.array(
        [
            [1, 1, 1],
            [1, 1, 1],
        ],
        dtype=np.int64,
    )

    result = run_bfs(grid=grid, start=(0, 0), end=(1, 2))

    assert result.path_found is True
    assert result.path == [(0, 0), (0, 1), (0, 2), (1, 2)]
    assert result.total_cost == 3
    assert result.path_length == 3
    assert result.runtime_ms >= 0


def test_run_bfs_returns_no_path_when_destination_is_unreachable() -> None:
    """BFS should fail cleanly when no route exists."""

    grid = np.array(
        [
            [1, 0],
            [0, 1],
        ],
        dtype=np.int64,
    )

    result = run_bfs(grid=grid, start=(0, 0), end=(1, 1))

    assert result.path_found is False
    assert result.path == []
    assert result.total_cost is None
    assert result.path_length == 0
    assert result.visited_nodes == 1
    assert result.runtime_ms >= 0


def test_run_bfs_handles_the_trivial_start_equals_end_case() -> None:
    """BFS should return immediately when the start and end are identical."""

    grid = np.array(
        [
            [5, 1],
            [1, 1],
        ],
        dtype=np.int64,
    )

    result = run_bfs(grid=grid, start=(0, 0), end=(0, 0))

    assert result.path_found is True
    assert result.path == [(0, 0)]
    assert result.total_cost == 0
    assert result.path_length == 0
    assert result.visited_nodes == 1
    assert result.runtime_ms >= 0
