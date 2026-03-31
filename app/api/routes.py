"""Top-level API routes."""

from fastapi import APIRouter, HTTPException, status

from app.algorithms import PathfindingResult
from app.core.config import APP_TITLE, APP_VERSION
from app.schemas import (
    AlgorithmChoice,
    Coordinate,
    PathRequest,
    PathResponse,
    RandomMapRequest,
    RandomMapResponse,
    SampleMapsResponse,
    ServiceInfoResponse,
)
from app.services import (
    AlgorithmNotImplementedError,
    generate_random_map,
    list_sample_maps,
    solve_path,
)

router = APIRouter()


@router.get("/", response_model=ServiceInfoResponse, tags=["meta"])
def read_root() -> ServiceInfoResponse:
    """Return basic service metadata for health checks and discovery."""

    return ServiceInfoResponse(name=APP_TITLE, version=APP_VERSION, status="ok")


@router.get("/maps/sample", response_model=SampleMapsResponse, tags=["maps"])
def get_sample_maps() -> SampleMapsResponse:
    """Return predefined sample maps for local experimentation."""

    return list_sample_maps()


@router.post("/maps/random", response_model=RandomMapResponse, tags=["maps"])
def create_random_map(request: RandomMapRequest) -> RandomMapResponse:
    """Generate a random weighted map with reproducible configuration."""

    return generate_random_map(request)


@router.post("/path", response_model=PathResponse, tags=["pathfinding"])
def find_path(request: PathRequest) -> PathResponse:
    """Run the requested pathfinding algorithm for a validated grid payload."""

    try:
        result = solve_path(request)
    except AlgorithmNotImplementedError as error:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail=str(error),
        ) from error

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
