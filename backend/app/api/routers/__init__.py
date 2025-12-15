"""API router initialization module."""

from fastapi import APIRouter
from .items import items_router

api_router = APIRouter()
api_router.include_router(items_router)
