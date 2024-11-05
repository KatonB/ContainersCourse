from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Response, status
from db.database import get_db
from store.queries import create_cart, get_cart, get_carts, add_item_to_cart
from api.shop_v1.contracts import CartResponse, CartItemResponse, CartListFilters, CartAddItemRequest

router = APIRouter()


@router.post("/", response_model=CartResponse, status_code=status.HTTP_201_CREATED)
def create_new_cart(response: Response, db: Session = Depends(get_db)):
    cart = create_cart(db)
    response.headers["Location"] = f"/cart/{cart.id}"
    return CartResponse.from_entity(cart)


@router.get("/{cart_id}", response_model=CartResponse)
def read_cart(cart_id: int, db: Session = Depends(get_db)):
    cart = get_cart(db, cart_id)
    if cart is None:
        raise HTTPException(status_code=404, detail="Cart not found")
    return CartResponse.from_entity(cart)


@router.get("/", response_model=list[CartResponse])
def read_carts(filters: CartListFilters = Depends(), db: Session = Depends(get_db)):
    carts = get_carts(db, filters)
    return [CartResponse.from_entity(cart) for cart in carts]


@router.post("/{cart_id}/add/{item_id}", response_model=CartItemResponse)
def add_item(cart_id: int, item_id: int, item_data: CartAddItemRequest, db: Session = Depends(get_db)):
    cart_item = add_item_to_cart(db, cart_id, item_id, item_data)
    if cart_item is None:
        raise HTTPException(status_code=404, detail="Cart or Item not found")
    return CartItemResponse.from_entity(cart_item)