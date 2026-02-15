import datetime
from typing import List
from sqlalchemy import Integer,ForeignKey, DateTime, func, UniqueConstraint
from cart.infra.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Cart(Base):
	__tablename__ = "cart_table"

	id: Mapped[int] = mapped_column(Integer,autoincrement=True,primary_key=True, nullable=False)
	customer_id: Mapped[int]=mapped_column(Integer)
	created_at: Mapped[datetime.datetime]=mapped_column(DateTime(timezone=True), server_default=func.now())
	updated_at: Mapped[datetime.datetime]=mapped_column(DateTime, nullable=False)
	details: Mapped[List["CartDetail"]] =relationship(back_populates="cart", cascade="all, delete")


class CartDetail(Base):

	__tablename__ = "cart_detail_table"

	id: Mapped[int] = mapped_column(Integer,autoincrement=True,primary_key=True)
	cart_id: Mapped[int]=mapped_column(ForeignKey(column="cart_table.id"))
	created_at: Mapped[datetime.datetime]=mapped_column(DateTime(timezone=True), server_default=func.now())
	product_id: Mapped[int]=mapped_column(Integer, nullable=False)
	quantity: Mapped[int]=mapped_column(Integer, nullable=False)
	cart: Mapped["Cart"] =relationship(back_populates="details")
	__table_args__ = (UniqueConstraint("cart_id","product_id", name="cart_migration_logs"),)

