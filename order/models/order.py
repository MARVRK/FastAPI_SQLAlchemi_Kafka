import uuid
from typing import List
from order.domain.enums import OrderStatus, get_statuses
from decimal import Decimal
from sqlalchemy import Integer, UUID, ForeignKey, DECIMAL, Enum
from order.infra.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UniqueConstraint

class Order(Base):
	__tablename__ = "orders"

	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	order_number: Mapped[uuid.UUID]= mapped_column(UUID(as_uuid=True), nullable=False)
	user_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
	order_items: Mapped[List["ProductsInOrder"]] = relationship("ProductsInOrder",back_populates="order", passive_deletes=True)
	status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus, values_callable = get_statuses, native_enum = True), nullable=False)
	__table_args__=(UniqueConstraint("order_number", name="order_order_number"),)

class ProductsInOrder(Base):
	__tablename__ = "products_in_order"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
	order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
	product_id: Mapped[int] = mapped_column(Integer, nullable=False)
	quantity: Mapped[int] = mapped_column(Integer,nullable=False, default=1)
	price_at_time: Mapped[Decimal] = mapped_column(DECIMAL(scale=2,precision=10),nullable=False)
	order: Mapped["Order"] = relationship("Order", back_populates="order_items")
	__table_args__ = (UniqueConstraint("order_id","product_id", name="products_in_order_id_product_id"),)