"""Lifespan management for the FastAPI app."""

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from .database import engine


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Manage the database engine lifespan."""
    await engine.connect()
    yield
    await engine.dispose()
