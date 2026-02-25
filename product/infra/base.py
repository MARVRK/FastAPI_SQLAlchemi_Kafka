from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from product.infra.settings import settings
from sqlalchemy.orm import DeclarativeBase

async_engine = create_async_engine(url=settings.PG_CONNECTION_PRODUCTS)
AsyncSessionLocal = async_sessionmaker(bind=async_engine)

async def get_db():
	db = AsyncSessionLocal()
	try:
		yield db
	finally:
		await db.close()

class Base(DeclarativeBase):
	pass
