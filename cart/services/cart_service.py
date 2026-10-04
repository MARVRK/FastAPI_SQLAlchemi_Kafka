from cart.repositories.cart_repo import CartRepository
from cart.schemas.requests import CartProduct
from cart.schemas.responses import CartResponse
from sqlalchemy.ext.asyncio import AsyncSession

class CartService:
    def __init__(self, repo: CartRepository, db: AsyncSession):
        self.repo = repo
        self.db = db

    async def create_replace_cart(self, customer_id: int, items: list[CartProduct]) -> CartResponse:
        cart_id = await self.repo.save_update_cart(customer_id=customer_id,
                                                    items=items,
                                                    db=self.db)
        await self.db.commit()
        return CartResponse(id=cart_id,items=items)

    async def delete_cart(self, customer_id: int) -> bool:
        delete_cart = await self.repo.delete_cart(customer_id=customer_id,
                                                  db=self.db)
        await self.db.commit()
        return delete_cart

    async def get_cart(self, customer_id: int) -> CartResponse:
        get_cart = await self.repo.get_cart(customer_id=customer_id,
                                            db=self.db)
        if get_cart is None:
            return CartResponse(id=None,items=[])
        return CartResponse(id=get_cart.id,items=get_cart.details)