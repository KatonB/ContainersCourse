from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, event

Base = declarative_base()


class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    deleted = Column(Boolean, default=False, index=True)  # добавлен индекс для быстрого поиска

    def __repr__(self):
        return f"<Item(id={self.id}, name='{self.name}', price={self.price}, deleted={self.deleted})>"


class CartItem(Base):
    __tablename__ = 'cart_items'

    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey('carts.id', ondelete="CASCADE"))
    item_id = Column(Integer, ForeignKey('items.id'))
    quantity = Column(Integer, default=1)

    cart = relationship("Cart", back_populates="items")
    item = relationship("Item")

    @property
    def available(self):
        return not self.item.deleted

    def __repr__(self):
        return f"<CartItem(cart_id={self.cart_id}, item_id={self.item_id}, quantity={self.quantity}, available={self.available}))>"

    @property
    def subtotal(self):
        """Расчет стоимости товаров в позиции."""
        return self.item.price * self.quantity



class Cart(Base):
    __tablename__ = 'carts'

    id = Column(Integer, primary_key=True, index=True)
    price = Column(Float, default=0.0)
    items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Cart(id={self.id}, price={self.price})>"

    def update_price(self):
        """Пересчет итоговой стоимости корзины."""
        self.price = sum(item.subtotal for item in self.items)


@event.listens_for(CartItem, 'after_insert')
@event.listens_for(CartItem, 'after_update')
@event.listens_for(CartItem, 'after_delete')
def update_cart_price(mapper, connection, target):
    cart = target.cart
    if cart:
        cart.update_price()
