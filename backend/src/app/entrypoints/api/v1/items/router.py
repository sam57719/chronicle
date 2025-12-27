"""Items router module."""

from fastapi import APIRouter, Depends, status

from app.features.items.application.services import ItemService
from .dependencies import get_item_service
from .schemas import ItemCreate, ItemRead

router = APIRouter(prefix="/items", tags=["Items"])


@router.post("/", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
async def create_item(
    payload: ItemCreate, service: ItemService = Depends(get_item_service)
):
    """Creates a new item with the provided payload."""
    item = service.create_item(name=payload.name, description=payload.description)
    return ItemRead(id=str(item.id), name=item.name, description=item.description)


@router.get("/", response_model=list[ItemRead])
async def list_items(service: ItemService = Depends(get_item_service)):
    """Lists all items."""
    items = service.list_items()
    return [
        ItemRead(id=str(i.id), name=i.name, description=i.description) for i in items
    ]
