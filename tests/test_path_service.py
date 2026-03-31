"""Tests for the pathfinding service layer."""

from app.schemas import AlgorithmChoice, Coordinate, PathRequest
from app.services import solve_path


def test_solve_path_dispatches_to_bfs() -> None:
    """The service should delegate BFS requests to the BFS algorithm."""

    request = PathRequest(
        grid=[
            [1, 1, 1],
            [0, 1, 1],
        ],
        start=Coordinate(row=0, col=0),
        end=Coordinate(row=1, col=2),
        algorithm=AlgorithmChoice.BFS,
    )

    result = solve_path(request)

    assert result.path_found is True
    assert result.path == [(0, 0), (0, 1), (0, 2), (1, 2)]
    assert result.total_cost == 3
    assert result.path_length == 3


def test_solve_path_dispatches_to_weighted_algorithms_consistently() -> None:
    """The service should delegate Dijkstra and A* without changing semantics."""

    base_request = dict(
        grid=[
            [1, 9, 1],
            [1, 9, 1],
            [1, 1, 1],
        ],
        start=Coordinate(row=0, col=0),
        end=Coordinate(row=0, col=2),
    )

    dijkstra_result = solve_path(
        PathRequest(algorithm=AlgorithmChoice.DIJKSTRA, **base_request)
    )
    astar_result = solve_path(
        PathRequest(algorithm=AlgorithmChoice.ASTAR, **base_request)
    )

    assert dijkstra_result.path_found is True
    assert dijkstra_result.path == astar_result.path
    assert dijkstra_result.total_cost == astar_result.total_cost == 6
    assert dijkstra_result.path_length == astar_result.path_length == 6
