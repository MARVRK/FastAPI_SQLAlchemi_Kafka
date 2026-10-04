from cart.error.error import CartError
from cart.models.cart import Cart
from cart.repositories.cart_repo import CartRepository, CartId
from cart.schemas.requests import CartCreateUpdate
from cart.schemas.responses import CartResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

class CartService:
    def __init__(self, repo: CartRepository, db: AsyncSession):
        self.repo = repo
        self.db = db

    async def create_replace_cart(self, customer_id: int, items: CartCreateUpdate) -> CartId:
        try:
            cart = await self.repo.save_update_cart(customer_id=customer_id,
                                                    items=items,
                                                    db=self.db)
            await self.db.commit()
            return cart
        except IntegrityError:
            raise

    async def delete_cart(self, customer_id: int) -> bool:
        delete_cart = await self.repo.delete_cart(customer_id=customer_id,
                                                  db=self.db)
        await self.db.commit()
        return delete_cart

    async def get_cart(self, customer_id: int) -> CartResponse:
        get_cart = await self.repo.get_cart(customer_id=customer_id,
                                            db=self.db)
        if not get_cart:
            return CartResponse(id=get_cart.id,items=[])
        return CartResponse(id=get_cart.id,items=get_cart.details)