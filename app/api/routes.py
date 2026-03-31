"""Top-level API routes."""

from fastapi import APIRouter, HTTPException, status

from app.algorithms import PathfindingResult, run_astar, run_bfs, run_dijkstra
from app.core.config import APP_TITLE, APP_VERSION
from app.schemas import (
    AlgorithmChoice,
    Coordinate,
    PathRequest,
    PathResponse,
    ServiceInfoResponse,
)

router = APIRouter()


@router.get("/", response_model=ServiceInfoResponse, tags=["meta"])
def read_root() -> ServiceInfoResponse:
    """Return basic service metadata for health checks and discovery."""

    return ServiceInfoResponse(name=APP_TITLE, version=APP_VERSION, status="ok")


@router.post("/path", response_model=PathResponse, tags=["pathfinding"])
def find_path(request: PathRequest) -> PathResponse:
    """Run the requested pathfinding algorithm for a validated grid payload."""

    if request.algorithm == AlgorithmChoice.BFS:
        result = run_bfs(
            grid=request.to_numpy(),
            start=request.start.as_tuple(),
            end=request.end.as_tuple(),
        )
    elif request.algorithm == AlgorithmChoice.DIJKSTRA:
        result = run_dijkstra(
            grid=request.to_numpy(),
            start=request.start.as_tuple(),
            end=request.end.as_tuple(),
        )
    elif request.algorithm == AlgorithmChoice.ASTAR:
        result = run_astar(
            grid=request.to_numpy(),
            start=request.start.as_tuple(),
            end=request.end.as_tuple(),
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail=f"Algorithm '{request.algorithm.value}' is not implemented yet.",
        )

    return _to_path_response(request.algorithm, result)


def _to_path_response(
    algorithm: AlgorithmChoice, result: PathfindingResult
) -> PathResponse:
    """Convert an internal algorithm result into the API response model."""

    return PathResponse(
        algorithm=algorithm,
        path=[Coordinate(row=row, col=col) for row, col in result.path],
        path_found=result.path_found,
        total_cost=result.total_cost,
        path_length=result.path_length,
        visited_nodes=result.visited_nodes,
        runtime_ms=result.runtime_ms,
    )
