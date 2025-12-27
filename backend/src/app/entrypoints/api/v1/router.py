"""Main Hub for all V1 API routes."""

from fastapi import APIRouter
from app.entrypoints.api.v1.items.router import router as items_router

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(items_router)
