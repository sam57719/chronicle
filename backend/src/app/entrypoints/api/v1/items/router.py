"""Items router module."""

from fastapi import APIRouter, Depends, status, HTTPException

from app.features.items.application.services import ItemService
from .dependencies import get_item_service
from .schemas import ItemCreate, ItemRead
from app.features.items.domain.value_objects import ItemID
from app.shared.domain.exceptions import InvalidDomainId

router = APIRouter(prefix="/items", tags=["Items"])


@router.post("/", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
async def create_item(
    payload: ItemCreate, service: ItemService = Depends(get_item_service)
):
    """Creates a new item with the provided payload."""
    item = await service.create_item(name=payload.name, description=payload.description)
    return ItemRead(id=str(item.id), name=item.name, description=item.description)


@router.get("/", response_model=list[ItemRead])
async def list_items(service: ItemService = Depends(get_item_service)):
    """Lists all items."""
    items = await service.list_items()
    return [
        ItemRead(id=str(i.id), name=i.name, description=i.description) for i in items
    ]


@router.get("/{item_id}", response_model=ItemRead)
async def get_item(item_id: str, service: ItemService = Depends(get_item_service)):
    """Retrieves a specific item."""
    try:
        domain_id = ItemID.from_str(item_id)
        item = await service.get_item(domain_id)

        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
            )

        return ItemRead(id=str(item.id), name=item.name, description=item.description)

    except InvalidDomainId as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
