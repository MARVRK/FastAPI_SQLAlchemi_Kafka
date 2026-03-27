from typing import List
from sqlalchemy import Integer, String, UUID, ForeignKey
from order.infra.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UniqueConstraint

class Order(Base):
	__tablename__ = "orders"

	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	order_number: Mapped[UUID]= mapped_column(UUID(as_uuid=True))
	user_id: Mapped[int] = mapped_column(Integer)
	order_items: Mapped[List["ProductsInOrder"]] = relationship("ProductsInOrder",back_populates="order", passive_deletes=True)
	status: Mapped[str] = mapped_column(String(20))
	total_price: Mapped[int] = mapped_column(nullable=False, default=0)
	__table_args__=(UniqueConstraint("order_number", name="order_order_number"),)

class ProductsInOrder(Base):
	__tablename__ = "products_in_order"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
	order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
	product_id: Mapped[int] = mapped_column(Integer, nullable=False)
	quantity: Mapped[int] = mapped_column(Integer,nullable=False, default=1)
	price_at_time: Mapped[float]
	order: Mapped["Order"] = relationship("Order", back_populates="order_items")
	__table_args__ = (UniqueConstraint("product_id", "order_id", name="products_in_order_id_product_id"),)