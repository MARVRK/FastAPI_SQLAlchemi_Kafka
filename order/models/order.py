from typing import List
from sqlalchemy import Integer, String, UUID, ForeignKey
from order.infra.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Order(Base):
	__tablename__ = "orders"

	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	order_number: Mapped[str]= mapped_column(UUID(as_uuid=True))
	user_id: Mapped[int] = mapped_column(Integer)
	order_items: Mapped[List["ProductsInOrder"]] = relationship("ProductsInOrder",back_populates="order")
	status: Mapped[str] = mapped_column(String(20))
	total_price: Mapped[int] = mapped_column(nullable=False, default=0)

class ProductsInOrder(Base):
	__tablename__ = "products_in_order"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
	order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
	product_id: Mapped[int] = mapped_column(Integer, nullable=False)
	quantity: Mapped[int] = mapped_column(Integer,nullable=False, default=1)
	price_at_time: Mapped[float]
	order: Mapped["Order"] = relationship("Order", back_populates="order_items")