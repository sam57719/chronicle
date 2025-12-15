"""Main application module for the Chronicle backend."""

from fastapi import FastAPI
from app.api.routers import api_router


def create_app() -> FastAPI:
    """
    Create and configure an instance of the FastAPI application.

    Returns:
        FastAPI: The configured FastAPI application instance.
    """
    app = FastAPI(
        title="Menagerist Backend"
    )

    app.include_router(api_router, prefix="/api")

    app.openapi_tags = [
        {"name": "items", "description": "Operations related to items."},
    ]

    return app


menagerist = create_app()
