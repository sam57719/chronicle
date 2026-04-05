"""Main module for the API."""

from fastapi import FastAPI


def create_app() -> FastAPI:
    """Creates and configures the FastAPI application instance."""
    fastapi_app = FastAPI(
        title="Menagerist",
        docs_url="/api/docs",
        openapi_url="/api/openapi.json",
    )

    return fastapi_app
