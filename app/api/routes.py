"""Top-level API routes."""

from fastapi import APIRouter

from app.core.config import APP_TITLE, APP_VERSION

router = APIRouter()


@router.get("/", tags=["meta"])
def read_root() -> dict[str, str]:
    """Return basic service metadata for health checks and discovery."""

    return {
        "name": APP_TITLE,
        "version": APP_VERSION,
        "status": "ok",
    }
