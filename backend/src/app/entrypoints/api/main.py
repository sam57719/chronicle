"""Main module for the API."""

from fastapi import FastAPI
from app.entrypoints.api.v1.router import v1_router


def create_app() -> FastAPI:
    """Creates and configures the FastAPI application instance."""
    fastapi_app = FastAPI(title="Menagerist")
    fastapi_app.include_router(v1_router, prefix="/api")

    @fastapi_app.get("/health")
    def health():
        return {"status": "ok"}

    return fastapi_app


app = create_app()
