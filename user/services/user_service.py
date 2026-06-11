import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from user.error.error import UserError, AuthError
from user.models.user import User
from user.repositories.user_repo import UserRepository, RefreshTokenRepository
from user.schemas.requests import UserRegister, UserLogin, UserUpdate
from user.schemas.responses import UserResponse, TokenResponse
from user.utils.jwt import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
)


class UserService:
    def __init__(
        self,
        user_repo: UserRepository,
        token_repo: RefreshTokenRepository,
        db: AsyncSession,
    ):
        self.user_repo = user_repo
        self.token_repo = token_repo
        self.db = db

    async def register(self, data: UserRegister) -> UserResponse:
        existing = await self.user_repo.get_user_by_email(data.email, self.db)
        if existing:
            raise UserError(f"User with email {data.email} already exists")

        user = User(
            email=data.email,
            encrypted_password=hash_password(data.password),
            role="user",
        )
        created = await self.user_repo.create_user(user, self.db)
        await self.db.commit()
        return UserResponse.model_validate(created)

    async def login(self, data: UserLogin) -> TokenResponse:
        user = await self.user_repo.get_user_by_email(data.email, self.db)
        if not user or not verify_password(data.password, user.encrypted_password):
            raise AuthError("Invalid email or password")

        await self.token_repo.revoke_all_tokens(user.id, self.db)

        access_token = create_access_token(user.id, user.role)
        refresh_token, expires_at = create_refresh_token()

        await self.token_repo.save_token(user.id, refresh_token, expires_at, self.db)
        await self.db.commit()

        return TokenResponse(access_token=access_token, refresh_token=refresh_token)

    async def refresh_access_token(self, refresh_token: str) -> TokenResponse:
        token_record = await self.token_repo.get_token(refresh_token, self.db)
        if not token_record:
            raise AuthError("Invalid or revoked refresh token")

        now = datetime.datetime.now(datetime.UTC)
        if token_record.expires_at.replace(tzinfo=datetime.UTC) < now:
            raise AuthError("Refresh token expired")

        user = await self.user_repo.get_user_by_id(token_record.user_id, self.db)
        if not user:
            raise AuthError("User not found")

        await self.token_repo.revoke_token(refresh_token, self.db)

        new_access = create_access_token(user.id, user.role)
        new_refresh, expires_at = create_refresh_token()
        await self.token_repo.save_token(user.id, new_refresh, expires_at, self.db)
        await self.db.commit()

        return TokenResponse(access_token=new_access, refresh_token=new_refresh)

    async def logout(self, refresh_token: str) -> dict:
        await self.token_repo.revoke_token(refresh_token, self.db)
        await self.db.commit()
        return {"status": "ok", "message": "logged out"}

    async def get_me(self, user_id: int) -> UserResponse:
        user = await self.user_repo.get_user_by_id(user_id, self.db)
        if not user:
            raise UserError("User not found")
        return UserResponse.model_validate(user)

    async def update_user(self, user_id: int, data: UserUpdate) -> UserResponse:
        payload = data.model_dump(exclude_none=True)
        if not payload:
            raise UserError("No fields to update")
        updated = await self.user_repo.update_user(user_id, payload, self.db)
        if not updated:
            raise UserError(f"User with id {user_id} not found")
        await self.db.commit()
        return UserResponse.model_validate(updated)

