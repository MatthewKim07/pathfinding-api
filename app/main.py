"""FastAPI application entrypoint."""

from fastapi import FastAPI

from app.api.routes import router
from app.core.config import APP_DESCRIPTION, APP_TITLE, APP_VERSION


def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance."""

    application = FastAPI(
        title=APP_TITLE,
        version=APP_VERSION,
        description=APP_DESCRIPTION,
    )
    application.include_router(router)
    return application


app = create_app()
