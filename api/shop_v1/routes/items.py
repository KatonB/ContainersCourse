from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from store.queries import (
    add_item,
    get_item,
    get_items,
    update_item as u_i,
    patch_item as p_i,
    delete_item as d_i,
)
from db.database import get_db
from api.shop_v1.contracts import ItemRequest, ItemResponse, ItemPatchRequest, ItemListFilters

router = APIRouter()


@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(item_data: ItemRequest, db: Session = Depends(get_db)):
    item = add_item(db, item_data)
    return ItemResponse.from_entity(item)


@router.get("/{item_id}", response_model=ItemResponse)
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return ItemResponse.from_entity(item)


@router.get("/", response_model=list[ItemResponse])
def read_items(filters: ItemListFilters = Depends(), db: Session = Depends(get_db)):
    items = get_items(db, filters)
    return [ItemResponse.from_entity(item) for item in items]


@router.put("/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item_data: ItemRequest, db: Session = Depends(get_db)):
    item = u_i(db, item_id, item_data)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return ItemResponse.from_entity(item)


@router.patch("/{item_id}", response_model=ItemResponse)
def patch_item(item_id: int, patch_data: ItemPatchRequest, db: Session = Depends(get_db)):
    item = p_i(db, item_id, patch_data)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    elif item == 'not_modified':
        raise HTTPException(status_code=304, detail="Item not modified")
    return ItemResponse.from_entity(item)


@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    success = d_i(db, item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"detail": "Item deleted"}
