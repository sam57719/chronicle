"""Main module for the API."""

from fastapi import FastAPI

from app.shared.config import Settings, get_settings


def create_app() -> FastAPI:
    """Creates and configures the FastAPI application instance."""
    settings: Settings = get_settings()

    fastapi_app = FastAPI(
        title=settings.app_info.display_name + " API",
        version=str(settings.app_info.version),
        description=settings.app_info.description,
        license_info=settings.app_info.license.model_dump(),
        docs_url="/api/docs",
        openapi_url="/api/openapi.json",
    )

    return fastapi_app
