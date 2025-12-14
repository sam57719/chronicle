"""Items router module."""

from fastapi import APIRouter

items_router = APIRouter()


@items_router.get("/")
async def get_items() -> list:
    """Get all items."""
    return []


@items_router.get("/{item_id}")
async def get_item(item_id: int) -> dict:
    """Get an item by ID."""
    return {}
