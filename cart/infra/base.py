from contextlib import asynccontextmanager
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from cart.infra.settings import settings

class Base(DeclarativeBase):
	pass
class DBSessionConfig:
	def __init__(self, db_url: str):
		self._engine = create_async_engine(url=db_url, echo=True)
		self._sessionmaker = async_sessionmaker(bind=self._engine, autoflush=False, expire_on_commit=True)
	@asynccontextmanager
	async def session(self):
		if self._engine is None:
			raise Exception("DBSessionConfig is not established!")

		session = self._sessionmaker()
		try:
			yield session
		except Exception as e:
			await session.rollback()
			raise e
		finally:
			await session.close()

session_manager = DBSessionConfig(db_url=settings.PG_CONNECTION_CART)

async def get_db():
	async with session_manager.session() as session:
		yield session

