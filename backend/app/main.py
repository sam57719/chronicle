"""Main application module for the Menagerist backend."""

from fastapi import FastAPI
from .api.routers import api_router
from .core.lifespan import lifespan


def create_app() -> FastAPI:
    """
    Create and configure an instance of the FastAPI application.

    Returns:
        FastAPI: The configured FastAPI application instance.
    """
    fastapi_app = FastAPI(title="Menagerist Backend", lifecycle=lifespan)

    fastapi_app.include_router(api_router, prefix="/api")

    fastapi_app.openapi_tags = [
        {"name": "items", "description": "Operations related to items."},
    ]

    return fastapi_app


app = create_app()
