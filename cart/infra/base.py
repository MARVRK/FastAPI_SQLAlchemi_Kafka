from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine

from order.infra.settings import settings

engine = create_engine(settings.PG_CONNECTION_ORDERS)
SessionLocal = sessionmaker(engine)

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()
class Base(DeclarativeBase):
	pass