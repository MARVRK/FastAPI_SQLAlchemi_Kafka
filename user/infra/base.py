from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from user.infra.settings import settings


class Base(DeclarativeBase):
    pass


class DBSessionConfig:
    def __init__(self, db_url: str):
        if not db_url:
            raise ValueError("DB URL was not provided")
        self._engine = create_async_engine(url=db_url, echo=False)
        self._sessionmaker = async_sessionmaker(bind=self._engine, autoflush=False, expire_on_commit=False)

    @asynccontextmanager
    async def session(self):
        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


session_manager = DBSessionConfig(db_url=settings.PG_CONNECTION_USERS)


async def get_db():
    async with session_manager.session() as session:
        yield session
