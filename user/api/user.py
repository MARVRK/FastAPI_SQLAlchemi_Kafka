from fastapi import APIRouter

from user.dependencies.core import UserServiceDep, CurrentUserDep
from user.schemas.requests import UserRegister, UserLogin, UserUpdate
from user.schemas.responses import UserResponse, TokenResponse

router = APIRouter(prefix="/user")


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(data: UserRegister, service: UserServiceDep):
    return await service.register(data)


@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin, service: UserServiceDep):
    return await service.login(data)


@router.post("/refresh-access-token", response_model=TokenResponse)
async def refresh_access_token(refresh_token: str, service: UserServiceDep):
    return await service.refresh_access_token(refresh_token)


@router.post("/logout")
async def logout(refresh_token: str, service: UserServiceDep):
    return await service.logout(refresh_token)


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: CurrentUserDep, service: UserServiceDep):
    return await service.get_me(int(current_user["sub"]))


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, data: UserUpdate, current_user: CurrentUserDep, service: UserServiceDep):
    return await service.update_user(user_id, data)
