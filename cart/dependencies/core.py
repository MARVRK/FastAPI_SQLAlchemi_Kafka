from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from cart.infra.base import get_db
from cart.services.cart_service import CartService
from cart.repositories.cart_repo import CartRepository

def get_cart_service (db: AsyncSession = Depends (get_db)) -> CartService:
    cart_repo = CartRepository ()
    return CartService (repo=cart_repo, db=db)

CartServiceDep = Annotated[AsyncSession, Depends (get_cart_service)]
