"""Top-level API routes."""

from fastapi import APIRouter

from app.core.config import APP_TITLE, APP_VERSION
from app.schemas import ServiceInfoResponse

router = APIRouter()


@router.get("/", response_model=ServiceInfoResponse, tags=["meta"])
def read_root() -> ServiceInfoResponse:
    """Return basic service metadata for health checks and discovery."""

    return ServiceInfoResponse(name=APP_TITLE, version=APP_VERSION, status="ok")
