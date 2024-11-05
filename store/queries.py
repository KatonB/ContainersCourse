from sqlalchemy import func
from typing import Optional, List
from sqlalchemy.orm import Session
from store.models import Item, Cart, CartItem
from api.shop_v1.contracts import ItemRequest, ItemPatchRequest, CartAddItemRequest, CartListFilters, \
    ItemListFilters


def add_item(db: Session, item_data: ItemRequest) -> Item:
    item = Item(name=item_data.name, price=item_data.price)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def get_item(db: Session, item_id: int) -> Optional[Item]:
    return db.query(Item).filter(Item.id == item_id, Item.deleted == False).first()


def get_items(db: Session, filters: ItemListFilters) -> List[Item]:
    query = db.query(Item).filter(Item.deleted == (filters.show_deleted if filters.show_deleted else False))

    if filters.min_price is not None:
        query = query.filter(Item.price >= filters.min_price)
    if filters.max_price is not None:
        query = query.filter(Item.price <= filters.max_price)
    query = query.offset(filters.offset).limit(filters.limit)

    return query.all()


def update_item(db: Session, item_id: int, item_data: ItemRequest) -> Optional[Item]:
    item = db.query(Item).filter(Item.id == item_id, Item.deleted == False).first()
    if item:
        item.name = item_data.name
        item.price = item_data.price
        db.commit()
        db.refresh(item)
    return item


def patch_item(db: Session, item_id: int, patch_data: ItemPatchRequest) -> Optional[Item]:
    item = db.query(Item).filter(Item.id == item_id, Item.deleted == False).first()

    is_modified = False

    if item is not None and patch_data.name is not None:
        item.name = patch_data.name
        is_modified = True

    if item is not None and patch_data.price is not None:
        item.price = patch_data.price
        is_modified = True

    if not is_modified:
        return 'not_modified'

    db.commit()
    db.refresh(item)
    return item


def delete_item(db: Session, item_id: int) -> bool:
    item = db.query(Item).filter(Item.id == item_id).first()
    if item:
        item.deleted = True
        db.commit()
        return True
    return False


def create_cart(db: Session) -> Cart:
    cart = Cart()
    db.add(cart)
    db.commit()
    db.refresh(cart)
    return cart


def get_cart(db: Session, cart_id: int) -> Optional[Cart]:
    return db.query(Cart).filter(Cart.id == cart_id).first()


def get_carts(db: Session, filters: CartListFilters) -> List[Cart]:
    query = db.query(Cart)

    if filters.min_price is not None:
        query = query.filter(Cart.price >= filters.min_price)
    if filters.max_price is not None:
        query = query.filter(Cart.price <= filters.max_price)

    if filters.min_quantity is not None:
        query = query.join(Cart.items).group_by(Cart.id).having(func.sum(CartItem.quantity) >= filters.min_quantity)

    if filters.max_quantity is not None:
        query = query.join(Cart.items).group_by(Cart.id).having(func.sum(CartItem.quantity) <= filters.max_quantity)

    query = query.offset(filters.offset).limit(filters.limit)

    return query.all()


def add_item_to_cart(db: Session, cart_id: int, item_id: int, item_data: CartAddItemRequest) -> Optional[CartItem]:
    cart = get_cart(db, cart_id)
    if not cart:
        return None
    item = db.query(Item).filter(Item.id == item_id, Item.deleted == False).first()
    if not item:
        return None

    cart_item = CartItem(cart_id=cart_id, item_id=item_id, quantity=item_data.quantity)
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return cart_item
