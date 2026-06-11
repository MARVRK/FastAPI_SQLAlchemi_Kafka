from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from user.infra.base import get_db
from user.repositories.user_repo import UserRepository, RefreshTokenRepository
from user.services.user_service import UserService
from user.utils.jwt import decode_access_token

bearer_scheme = HTTPBearer()


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(
        user_repo=UserRepository(),
        token_repo=RefreshTokenRepository(),
        db=db,
    )


UserServiceDep = Annotated[UserService, Depends(get_user_service)]

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    return decode_access_token(credentials.credentials)


CurrentUserDep = Annotated[dict, Depends(get_current_user)]
