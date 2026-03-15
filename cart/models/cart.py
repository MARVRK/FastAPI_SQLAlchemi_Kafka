import datetime
from typing import List
from sqlalchemy import Integer,ForeignKey, DateTime, func, UniqueConstraint
from cart.infra.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Cart(Base):
	__tablename__ = "cart_table"

	id: Mapped[int] = mapped_column(Integer,autoincrement=True,primary_key=True)
	customer_id: Mapped[int]=mapped_column(Integer)
	created_at: Mapped[datetime.datetime]=mapped_column(DateTime(timezone=True), server_default=func.now())
	updated_at: Mapped[datetime.datetime]=mapped_column(DateTime(timezone=True), nullable=False)
	details: Mapped[List["CartDetail"]] =relationship(back_populates="cart", passive_deletes=True)
	__table_args__ = (UniqueConstraint("customer_id", name="cart_table_unique_customer_id"),)


class CartDetail(Base):

	__tablename__ = "cart_detail_table"

	id: Mapped[int] = mapped_column(Integer,autoincrement=True,primary_key=True)
	cart_id: Mapped[int]=mapped_column(ForeignKey(column="cart_table.id", ondelete="CASCADE"))
	created_at: Mapped[datetime.datetime]=mapped_column(DateTime(timezone=True), server_default=func.now())
	product_id: Mapped[int]=mapped_column(Integer, nullable=False)
	quantity: Mapped[int]=mapped_column(Integer, nullable=False)
	cart: Mapped["Cart"] =relationship(back_populates="details")
	__table_args__ = (UniqueConstraint("cart_id","product_id", name="cart_detail_cart_product_id"),)

