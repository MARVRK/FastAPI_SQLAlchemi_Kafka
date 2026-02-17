from typing import List

from sqlalchemy import func
from sqlalchemy.orm import selectinload
from abc import ABC, abstractmethod
from cart.models.cart import Cart, CartDetail
from cart.infra.base import session_manager
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio

class CartAbstraction (ABC):
	@abstractmethod
	async def get_cart (self, cart_id: int, db: AsyncSession) -> Cart | None:
		pass

	@abstractmethod
	async def create_cart (self, customer_id: int, db: AsyncSession, details: List[CartDetail]) -> Cart:
		pass

	@abstractmethod
	async def delete_cart (self, cart_id: int) -> Cart:
		pass

	@abstractmethod
	async def update_cart (self, cart_id) -> Cart | None:
		pass

class CartRepository (CartAbstraction):
	@classmethod
	async def get_cart (cls, cart_id: int, db: AsyncSession) -> Cart | None:
		result = await db.scalars (select (Cart).where (Cart.id == cart_id).options (selectinload (Cart.details)))
		cart = result.first ()
		if not cart:
			return None
		return Cart(id=cart.id,
		            customer_id=cart.customer_id,
		            details=cart.details)

	@classmethod
	async def create_cart (cls, customer_id: int, db: AsyncSession, details: List[CartDetail]):
		if details is None:
			await db.rollback ()
			raise "At least one product should be selected!!!"
		new_cart = Cart (customer_id=customer_id, updated_at=func.now (), details=[])
		db.add (new_cart)
		await db.commit ()  ##### remove it later service logic based from Medium Article

	async def delete_cart (self):
		pass

	async def update_cart (self):
		pass

async def main ():
	async with session_manager.session () as db:
		# await CartRepository.create_cart (customer_id=1, db=db, details=[])
		cp = await CartRepository.get_cart (cart_id=3, db=db)
		print (cp.id, cp.details, cp.customer_id)

asyncio.run (main ())
