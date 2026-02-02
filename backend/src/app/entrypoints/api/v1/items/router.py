"""Items router module."""

from fastapi import APIRouter, Depends, HTTPException, status

from app.features.items.application.use_cases.create_item import (
    CreateItem,
    CreateItemCommand,
)
from app.features.items.application.use_cases.get_item import GetItem, GetItemCommand
from app.features.items.application.use_cases.list_items import (
    ListItems,
    ListItemsCommand,
)
from app.features.items.domain.value_objects import ItemID
from app.shared.domain.exceptions import InvalidDomainId

from .dependencies import (
    get_create_item_use_case,
    get_get_item_use_case,
    get_list_items_use_case,
)
from .schemas import ItemCreate, ItemRead

router = APIRouter(prefix="/items", tags=["Items"])


@router.post("/", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
async def create_item(
    payload: ItemCreate, uc: CreateItem = Depends(get_create_item_use_case)
) -> ItemRead:
    """Creates a new item with the provided payload."""
    cmd = CreateItemCommand(name=payload.name, description=payload.description)
    item = await uc.execute(cmd)
    return ItemRead(id=str(item.id), name=item.name, description=item.description)


@router.get("/", response_model=list[ItemRead])
async def list_items(
    uc: ListItems = Depends(get_list_items_use_case),
) -> list[ItemRead]:
    """Lists all items."""
    items = await uc.execute(ListItemsCommand())
    return [
        ItemRead(id=str(i.id), name=i.name, description=i.description) for i in items
    ]


@router.get("/{item_id}", response_model=ItemRead)
async def get_item(
    item_id: str, uc: GetItem = Depends(get_get_item_use_case)
) -> ItemRead:
    """Retrieves a specific item."""
    try:
        domain_id = ItemID.create(item_id)
        item = await uc.execute(GetItemCommand(item_id=domain_id))

        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
            )

        return ItemRead(id=str(item.id), name=item.name, description=item.description)

    except InvalidDomainId as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
