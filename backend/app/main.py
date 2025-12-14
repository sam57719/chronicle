"""Main application module for the Chronicle backend."""

from fastapi import FastAPI


def create_app() -> FastAPI:
    """Create and configure an instance of the FastAPI application."""
    app = FastAPI()
    return app


chronicle = create_app()
