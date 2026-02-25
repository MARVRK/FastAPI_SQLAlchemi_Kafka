from sqlalchemy import Integer, String, Boolean, DateTime
from user.infra.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func, ForeignKey
import datetime


class User(Base):
	__tablename__ = "user"

	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	email: Mapped[str] = mapped_column(String(length=50), unique=True, nullable=False)
	encrypted_password: Mapped[str] = mapped_column(String(length=200))
	created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
	updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now())

class RefreshToken(Base):
	__tablename__ = "refresh_token"

	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	user_id: Mapped[int] = ForeignKey("user.id"), mapped_column(Integer, nullable=False)
	refresh_token: Mapped[str] = mapped_column(String)
	created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
	expires_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
	revoked: Mapped[bool] = mapped_column(Boolean, default=False)