from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from product.infra.Base import Base

class Product(Base):
	__tablename__ = "product"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
	product: Mapped[str] = mapped_column(String(length=50))
	available_amount: Mapped[int] = mapped_column(Integer,default=0)