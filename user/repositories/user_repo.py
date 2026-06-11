import datetime
from abc import ABC, abstractmethod

from sqlalchemy import select, delete, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from user.models.user import User, RefreshToken


class UserAbstraction(ABC):
    @abstractmethod
    async def get_user_by_id(self, user_id: int, db: AsyncSession) -> User | None:
        pass

    @abstractmethod
    async def get_user_by_email(self, email: str, db: AsyncSession) -> User | None:
        pass

    @abstractmethod
    async def create_user(self, user: User, db: AsyncSession) -> User:
        pass

    @abstractmethod
    async def update_user(self, user_id: int, data: dict, db: AsyncSession) -> User | None:
        pass

    @abstractmethod
    async def delete_user(self, user_id: int, db: AsyncSession) -> int:
        pass


class UserRepository(UserAbstraction):
    async def get_user_by_id(self, user_id: int, db: AsyncSession) -> User | None:
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str, db: AsyncSession) -> User | None:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create_user(self, user: User, db: AsyncSession) -> User:
        stmt = (
            insert(User)
            .values(email=user.email, encrypted_password=user.encrypted_password, role=user.role)
            .returning(User)
        )
        result = await db.execute(stmt)
        return result.scalar_one()

    async def update_user(self, user_id: int, data: dict, db: AsyncSession) -> User | None:
        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(**data)
            .returning(User)
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def delete_user(self, user_id: int, db: AsyncSession) -> int:
        await db.execute(delete(User).where(User.id == user_id))
        return user_id


class RefreshTokenRepository:
    async def save_token(
        self,
        user_id: int,
        token: str,
        expires_at: datetime.datetime,
        db: AsyncSession,
    ) -> RefreshToken:
        stmt = (
            insert(RefreshToken)
            .values(user_id=user_id, refresh_token=token, expires_at=expires_at)
            .returning(RefreshToken)
        )
        result = await db.execute(stmt)
        return result.scalar_one()

    async def get_token(self, token: str, db: AsyncSession) -> RefreshToken | None:
        result = await db.execute(
            select(RefreshToken).where(
                RefreshToken.refresh_token == token,
                RefreshToken.revoked.is_(False),
            )
        )
        return result.scalar_one_or_none()

    async def revoke_token(self, token: str, db: AsyncSession) -> None:
        result = await db.execute(
            select(RefreshToken).where(RefreshToken.refresh_token == token)
        )
        refresh = result.scalar_one_or_none()
        if refresh:
            refresh.revoked = True
            db.add(refresh)

    async def revoke_all_tokens(self, user_id: int, db: AsyncSession) -> None:
        await db.execute(
            update(RefreshToken)
            .where(RefreshToken.user_id == user_id, RefreshToken.revoked.is_(False))
            .values(revoked=True)
        )
