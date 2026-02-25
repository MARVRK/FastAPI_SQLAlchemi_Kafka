from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from order.infra.settings import settings

engine = create_async_engine(url=settings.PG_CONNECTION_ORDERS)
SessionLocal = async_sessionmaker(bind=engine)

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()
class Base(DeclarativeBase):
	pass