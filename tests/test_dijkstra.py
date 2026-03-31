"""Unit tests for the Dijkstra pathfinding implementation."""

import numpy as np

from app.algorithms import run_bfs, run_dijkstra


def test_run_dijkstra_returns_the_lowest_cost_path_on_a_weighted_grid() -> None:
    """Dijkstra should minimize total traversal cost on weighted maps."""

    grid = np.array(
        [
            [1, 5, 1],
            [1, 1, 1],
            [9, 9, 1],
        ],
        dtype=np.int64,
    )

    result = run_dijkstra(grid=grid, start=(0, 0), end=(0, 2))

    assert result.path_found is True
    assert result.path == [(0, 0), (1, 0), (1, 1), (1, 2), (0, 2)]
    assert result.total_cost == 4
    assert result.path_length == 4
    assert result.visited_nodes > 0
    assert result.runtime_ms >= 0


def test_run_dijkstra_prefers_lower_cost_over_the_bfs_shortest_step_route() -> None:
    """Dijkstra should beat BFS when the fewest-step path is more expensive."""

    grid = np.array(
        [
            [1, 9, 1],
            [1, 9, 1],
            [1, 1, 1],
        ],
        dtype=np.int64,
    )

    bfs_result = run_bfs(grid=grid, start=(0, 0), end=(0, 2))
    dijkstra_result = run_dijkstra(grid=grid, start=(0, 0), end=(0, 2))

    assert bfs_result.path == [(0, 0), (0, 1), (0, 2)]
    assert bfs_result.total_cost == 10
    assert dijkstra_result.path == [
        (0, 0),
        (1, 0),
        (2, 0),
        (2, 1),
        (2, 2),
        (1, 2),
        (0, 2),
    ]
    assert dijkstra_result.total_cost == 6
    assert dijkstra_result.path_length == 6
    assert dijkstra_result.runtime_ms >= 0


def test_run_dijkstra_returns_no_path_when_destination_is_unreachable() -> None:
    """Dijkstra should fail cleanly when no route exists."""

    grid = np.array(
        [
            [1, 0],
            [0, 1],
        ],
        dtype=np.int64,
    )

    result = run_dijkstra(grid=grid, start=(0, 0), end=(1, 1))

    assert result.path_found is False
    assert result.path == []
    assert result.total_cost is None
    assert result.path_length == 0
    assert result.visited_nodes == 1
    assert result.runtime_ms >= 0
