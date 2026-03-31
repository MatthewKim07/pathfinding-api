"""Service-layer orchestration for pathfinding requests."""

from __future__ import annotations

from collections.abc import Callable

import numpy as np
from numpy.typing import NDArray

from app.algorithms import PathfindingResult, run_astar, run_bfs, run_dijkstra
from app.schemas import AlgorithmChoice, GridProblem, PathRequest

AlgorithmRunner = Callable[
    [NDArray[np.int64], tuple[int, int], tuple[int, int]],
    PathfindingResult,
]

_ALGORITHM_RUNNERS: dict[AlgorithmChoice, AlgorithmRunner] = {
    AlgorithmChoice.BFS: run_bfs,
    AlgorithmChoice.DIJKSTRA: run_dijkstra,
    AlgorithmChoice.ASTAR: run_astar,
}


class AlgorithmNotImplementedError(RuntimeError):
    """Raised when a requested algorithm is not available in the service layer."""


def solve_path(request: PathRequest) -> PathfindingResult:
    """Dispatch a validated pathfinding request to the appropriate algorithm."""

    return solve_problem(request, request.algorithm)


def solve_problem(
    problem: GridProblem, algorithm: AlgorithmChoice
) -> PathfindingResult:
    """Dispatch a validated grid problem to the requested algorithm."""

    try:
        runner = _ALGORITHM_RUNNERS[algorithm]
    except KeyError as error:
        raise AlgorithmNotImplementedError(
            f"Algorithm '{algorithm.value}' is not implemented yet."
        ) from error

    return runner(
        grid=problem.to_numpy(),
        start=problem.start.as_tuple(),
        end=problem.end.as_tuple(),
    )
