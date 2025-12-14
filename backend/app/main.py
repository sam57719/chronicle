"""Main application module for the Chronicle backend."""

from fastapi import FastAPI


def create_app() -> FastAPI:
    """
    Create and configure an instance of the FastAPI application.

    Returns:
        FastAPI: The configured FastAPI application instance.
    """
    app = FastAPI()
    return app


chronicle = create_app()
