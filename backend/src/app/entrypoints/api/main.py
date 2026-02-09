"""Main module for the API."""

from fastapi import FastAPI

from app.entrypoints.api.exception_handlers import add_exception_handlers
from app.entrypoints.api.system.router import router as system_router
from app.entrypoints.api.v1.router import v1_router


def create_app() -> FastAPI:
    """Creates and configures the FastAPI application instance."""
    fastapi_app = FastAPI(
        title="Menagerist",
        docs_url="/api/docs",
        openapi_url="/api/openapi.json",
    )
    fastapi_app.include_router(system_router, prefix="/api")
    fastapi_app.include_router(v1_router, prefix="/api")

    add_exception_handlers(fastapi_app)

    fastapi_app.openapi_tags = [
        {
            "name": "System",
            "description": "Operations related to system management.",
        },
        {
            "name": "Items",
            "description": "Operations related to item management.",
        },
    ]

    return fastapi_app
