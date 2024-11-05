from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from store.models import Item, Cart, CartItem


class ItemRequest(BaseModel):
    name: str
    price: float

    def as_item(self) -> Item:
        return Item(name=self.name, price=self.price)


class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    deleted: bool

    @staticmethod
    def from_entity(entity: Item):
        return ItemResponse(
            id=entity.id,
            name=entity.name,
            price=entity.price,
            deleted=entity.deleted
        )


class ItemPatchRequest(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    class Config:
        extra = "forbid"


class CartItemResponse(BaseModel):
    id: int
    item_id: int
    name: str
    quantity: int
    available: bool

    @staticmethod
    def from_entity(entity: CartItem):
        return CartItemResponse(
            id=entity.id,
            item_id=entity.item_id,
            name=entity.item.name,
            quantity=entity.quantity,
            available=entity.available
        )


class CartResponse(BaseModel):
    id: int
    items: List[CartItemResponse]
    price: float

    @staticmethod
    def from_entity(entity: Cart):
        items = [CartItemResponse.from_entity(item) for item in entity.items]
        return CartResponse(id=entity.id, items=items, price=entity.price)


class CartCreateResponse(BaseModel):
    id: int


class CartAddItemRequest(BaseModel):
    quantity: int = Field(ge=1, description="Quantity of the item to add to the cart")

    model_config = ConfigDict(extra="forbid")



class CartListFilters(BaseModel):
    offset: Optional[int] = Field(0, ge=0, description="Offset for pagination")
    limit: Optional[int] = Field(10, gt=0, description="Limit for pagination")
    min_price: Optional[float] = Field(None, ge=0, description="Minimum price filter")
    max_price: Optional[float] = Field(None, ge=0, description="Maximum price filter")
    min_quantity: Optional[int] = Field(None, ge=0, description="Minimum quantity filter")
    max_quantity: Optional[int] = Field(None, ge=0, description="Maximum quantity filter")

    model_config = ConfigDict(extra="forbid")


class ItemListFilters(BaseModel):
    offset: Optional[int] = Field(0, ge=0, description="Offset for pagination")
    limit: Optional[int] = Field(10, gt=0, description="Limit for pagination")
    min_price: Optional[float] = Field(None, ge=0, description="Minimum price filter")
    max_price: Optional[float] = Field(None, ge=0, description="Maximum price filter")
    show_deleted: Optional[bool] = Field(False, description="Show deleted items")

    model_config = ConfigDict(extra="forbid")