from sqlalchemy import func
from abc import ABC, abstractmethod
from cart.error.error import CartError
from cart.models.cart import Cart, CartDetail
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import selectinload
from sqlalchemy import delete, select
from cart.schemas.requests import CartCreateUpdate
from cart.schemas.responses import CartResponse

CartId = int
class CartAbstraction (ABC):

    @abstractmethod
    async def get_cart (self, customer_id: int, db: AsyncSession) -> CartResponse:
        pass

    @abstractmethod
    async def save_update_cart (self, customer_id:int, items: CartCreateUpdate, db: AsyncSession ) -> CartId :
        pass

    @abstractmethod
    async def delete_cart (self, customer_id: int, db: AsyncSession) -> bool:
        pass

class CartRepository (CartAbstraction):
    async def get_cart (self, customer_id: int, db: AsyncSession) -> CartResponse:
        '''
        SQL Request:
        NOT VALID - NEED TO CHANGE!!!!!!
        '''
        if not customer_id:
            raise CartError ("No customer_id provided")

        cart_stmt = select (Cart).options(selectinload(Cart.details)).where(Cart.customer_id == customer_id)
        cart = await db.execute (cart_stmt)
        return cart.scalar_one_or_none ()


    async def delete_cart (self, customer_id: int ,db: AsyncSession) -> bool:
        '''
        SQL Request:
        NOT VALID - NEED TO CHANGE!!!!!!
        '''

        if not customer_id:
            raise CartError ("No customer_id provided")

        cart_stmt = delete (Cart).where (Cart.customer_id == customer_id)
        deleted_cart = await db.execute (cart_stmt)
        return deleted_cart.rowcount > 0

    async def save_update_cart (self, customer_id: int, items: CartCreateUpdate, db: AsyncSession) -> CartId:
        '''
        SQL Request:
        NOT VALID - NEED TO CHANGE!!!!!!
        '''

        if not customer_id:
            raise CartError ("No customer_id provided")

        #updating/creating a new Сart
        cart_stmt = insert (Cart).values (customer_id = customer_id, updated_at = func.now())
        cart_stmt = cart_stmt.on_conflict_do_update(constraint="cart_table_unique_customer_id",
                                                    set_=dict(updated_at=func.now())).returning(Cart.id)
        get_cart_id = await db.execute (cart_stmt)
        cart_id = get_cart_id.scalar_one()

        #delete old CartDetails with items
        delete_old_items = delete(CartDetail).where(CartDetail.cart_id == cart_id)
        await db.execute(delete_old_items)

        #creating new CartDetails with new values
        cart_details = [{"cart_id": cart_id, "product_id": item.product_id, "quantity": item.quantity} for item in items]
        cart_detail_stmt = insert(CartDetail).values(cart_details)
        await db.execute(cart_detail_stmt)

        return cart_id

