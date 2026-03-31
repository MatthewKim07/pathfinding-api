"""Service-layer orchestration for pathfinding requests."""

from __future__ import annotations

from collections.abc import Callable

import numpy as np
from numpy.typing import NDArray

from app.algorithms import PathfindingResult, run_astar, run_bfs, run_dijkstra
from app.schemas import AlgorithmChoice, PathRequest

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

    try:
        runner = _ALGORITHM_RUNNERS[request.algorithm]
    except KeyError as error:
        raise AlgorithmNotImplementedError(
            f"Algorithm '{request.algorithm.value}' is not implemented yet."
        ) from error

    return runner(
        grid=request.to_numpy(),
        start=request.start.as_tuple(),
        end=request.end.as_tuple(),
    )
