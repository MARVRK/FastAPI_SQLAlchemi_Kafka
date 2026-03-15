from contextlib import asynccontextmanager
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from cart.infra.settings import settings
from cart.error.error import CartError

class Base(DeclarativeBase):
	pass
class DBSessionConfig:
	def __init__(self, db_url: str):
		if not db_url:
			raise CartError(message="DBSessionConfig was not established or None")
		self._engine = create_async_engine(url=db_url, echo=False)
		self._sessionmaker = async_sessionmaker(bind=self._engine, autoflush=False, expire_on_commit=False)

	@asynccontextmanager
	async def session(self):
		session = self._sessionmaker()
		try:
			yield session
		except Exception as error:
			await session.rollback()
			raise CartError(message="DB_Session_Manager error", original_exception=error)
		finally:
			await session.close()

session_manager = DBSessionConfig(db_url=settings.PG_CONNECTION_CART)

async def get_db():
	async with session_manager.session() as session:
		yield session

