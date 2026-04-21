"""Main module for the API."""

from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

from fastapi import FastAPI

from app.shared.config import Settings, get_settings

from ...infrastructure.wiring import bootstrap
from .middlewares import (
    access_log_middleware,
    app_response_headers_middleware,
    request_id_middleware,
)
from .system.router import router as system_router
from .v1.router import v1_router

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

API_PREFIX = "/api"


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    """Application lifespan hook.

    The bootstrap startup/shutdown functions are asynchronous, so we must
    await them here. The function is an async generator decorated with
    `asynccontextmanager` which matches FastAPI's expected `lifespan` type.
    """
    settings: Settings = get_settings()

    await bootstrap.startup(settings)
    try:
        yield
    finally:
        await bootstrap.shutdown(settings)


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
        lifespan=lifespan,
    )

    fastapi_app.include_router(system_router, prefix=API_PREFIX)
    fastapi_app.include_router(v1_router, prefix=API_PREFIX)

    if settings.api.access_log_enabled:
        fastapi_app.middleware("http")(access_log_middleware)

    fastapi_app.middleware("http")(app_response_headers_middleware)

    # Ensure that the request id middleware is bound last
    fastapi_app.middleware("http")(request_id_middleware)

    fastapi_app.openapi_tags = [
        {"name": "System", "description": "System related endpoints"},
    ]

    return fastapi_app
