from sqlalchemy import String, Integer, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column
from product.infra.base import Base

class Product(Base):
	__tablename__ = "product"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
	product: Mapped[str] = mapped_column(String(length=50), unique=True)
	available_amount: Mapped[int] = mapped_column(Integer,default=0)
	current_price: Mapped[DECIMAL] = mapped_column(DECIMAL(scale=10,precision=2),nullable=False)