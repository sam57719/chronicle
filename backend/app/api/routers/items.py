"""Items router module."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.item import ItemRead, ItemCreate, ItemUpdate
from app.services.item_service import ItemService
from ..deps import get_async_db_session  # your async session dependency

ITEM_NOT_FOUND_RESPONSE = {
    404: {
        "description": "Item not found",
        "content": {
            "application/json": {
                "example": {"detail": "Item not found"},
            },
        },
    },
}

class ItemNotFound(HTTPException):
    """Raised when an item cannot be found."""

    def __init__(self) -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")


items_router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses=ITEM_NOT_FOUND_RESPONSE,
)


def get_item_service(db: AsyncSession = Depends(get_async_db_session)) -> ItemService:
    """Factory for ItemService with a database session."""
    return ItemService(db)


@items_router.get("/", response_model=List[ItemRead])
async def list_items(
    service: ItemService = Depends(get_item_service),
) -> List[ItemRead]:
    """List all items."""
    return await service.list_items()


@items_router.get("/{item_id}", response_model=ItemRead)
async def get_item(
    item_id: int, service: ItemService = Depends(get_item_service)
) -> ItemRead:
    """Retrieve a single item by ID."""
    item = await service.get_item(item_id)
    if item is None:
        raise ItemNotFound()
    return item


@items_router.post("/", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
async def create_item(
    data: ItemCreate, service: ItemService = Depends(get_item_service)
) -> ItemRead:
    """Create a new item."""
    return await service.create_item(data)


@items_router.put("/{item_id}", response_model=ItemRead)
async def update_item(
    item_id: int, data: ItemUpdate, service: ItemService = Depends(get_item_service)
) -> ItemRead:
    """Update an existing item."""
    item = await service.update_item(item_id, data)
    if item is None:
        raise ItemNotFound()
    return item


@items_router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: int, service: ItemService = Depends(get_item_service)
) -> None:
    """Delete an item."""
    deleted = await service.delete_item(item_id)
    if not deleted:
        raise ItemNotFound()
