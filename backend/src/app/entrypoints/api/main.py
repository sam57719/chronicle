"""Main module for the API."""

from fastapi import FastAPI

from app.shared.config import Settings, get_settings

from .system.router import router as system_router
from .v1.router import v1_router

API_PREFIX = "/api"


def create_app() -> FastAPI:
    """Creates and configures the FastAPI application instance."""
    settings: Settings = get_settings()

    fastapi_app = FastAPI(
        title=settings.app.display_name + " API",
        version=settings.app.version,
        description=settings.app.description,
        license_info=settings.app.license.model_dump(),
        docs_url=f"{API_PREFIX}/docs",
        openapi_url=f"{API_PREFIX}/openapi.json",
        redoc_url=None,
    )

    fastapi_app.include_router(system_router, prefix=API_PREFIX)
    fastapi_app.include_router(v1_router, prefix=API_PREFIX)

    fastapi_app.openapi_tags = [
        {"name": "System", "description": "System related endpoints"},
    ]

    return fastapi_app
