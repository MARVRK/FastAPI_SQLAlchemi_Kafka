from sqlalchemy import func
from abc import ABC, abstractmethod
from cart.error.error import CartError
from cart.models.cart import Cart, CartDetail
from cart.infra.base import session_manager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import selectinload
from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
import asyncio

class CartAbstraction (ABC):

    @abstractmethod
    async def get_cart (self, cart_id: int, db: AsyncSession) -> Cart | None:
        pass

    @abstractmethod
    async def save_update_cart (self, cart: Cart, db: AsyncSession | None) -> Cart.id:
        pass

    @abstractmethod
    async def delete_cart (self, cart_id: int, db: AsyncSession) -> None | dict[str, str]:
        pass

class CartRepository (CartAbstraction):
    async def get_cart (self, cart_id: int, db: AsyncSession) -> Cart | None:
        '''
        SQL Request:
        This is request to table -> Cart
        SELECT cart_table.id, cart_table.customer_id, cart_table.created_at, cart_table.updated_at
        WHERE cart_table.id = $1::INTEGER

        This is request to table -> CartDetail
        SELECT cart_detail_table.cart_id AS cart_detail_table_cart_id,
               cart_detail_table.id AS cart_detail_table_id,
               cart_detail_table.created_at AS cart_detail_table_created_at,
               cart_detail_table.product_id AS cart_detail_table_product_id,
               cart_detail_table.quantity AS cart_detail_table_quantity
        FROM cart_detail_table
        WHERE cart_detail_table.cart_id IN ($1::INTEGER)
        '''
        if not cart_id:
            return None
        cart_stmt = select (Cart).options (selectinload (Cart.details)).where (Cart.id == cart_id)
        cart = await db.execute (cart_stmt)
        return cart.scalar_one_or_none ()

    async def save_update_cart (self, cart: Cart, db: AsyncSession) -> Cart.id:
        '''
        SQL Request:
        This is request to table -> Cart
        INSERT INTO cart_table (customer_id, updated_at) VALUES ($1::INTEGER, now()) ON CONFLICT ON CONSTRAINT cart_table_unique_customer_id DO
        UPDATE SET updated_at = now() RETURNING cart_table.id
        ON CONFLICT ON CONSTRAINT cart_table_unique_customer_id
        DO UPDATE SET updated_at = now() RETURNING cart_table.id

        This is request to table -> CartDetail
        INSERT INTO cart_detail_table (cart_id, product_id, quantity) VALUES ($1::INTEGER, $2::INTEGER, $3::INTEGER)
        ON CONFLICT ON CONSTRAINT cart_detail_cart_product_id DO UPDATE SET quantity = $4::INTEGER
        RETURNING cart_detail_table.id
        '''

        if not cart.details:
            raise CartError ("At least one product should be added")
        try:
            cart_stmt = insert (Cart).values (customer_id=cart.customer_id, updated_at=cart.updated_at)
            cart_stmt = (
                cart_stmt.on_conflict_do_update (constraint="cart_table_unique_customer_id", set_=dict (updated_at=func.now ())).returning (Cart.id))
            result = await db.execute (cart_stmt)
            # getting id of updated or new created card.id
            card_id_form_result = result.scalar_one ()

            # creating list of data from cart.details
            card_details = [{"cart_id": card_id_form_result, "product_id": d.product_id, "quantity": d.quantity} for d in cart.details]
            # push one bulk insert on DB by one execution
            data_stmt = insert (CartDetail).values (card_details)
            data_stmt = data_stmt.on_conflict_do_update (constraint="cart_detail_cart_product_id", set_=dict (quantity=data_stmt.excluded.quantity))
            await db.execute (data_stmt)

            return card_id_form_result
        except IntegrityError as error:
            raise CartError (f"Failed to save/update cart", original_exception=error)

    async def delete_cart (self, cart: Cart, db: AsyncSession) -> None | dict[str, str]:
        '''
        SQL Request:
        DELETE FROM cart_table WHERE cart_table.id = $1::INTEGER
        Cascade delete method was enabled in models.cart
        '''
        if cart is None:
            return None
        cart_stmt = delete (Cart).where (Cart.id == cart.id)
        await db.execute (cart_stmt)
        return {"DB_CART": f"Cart with id {cart.id} was deleted from DB"}
