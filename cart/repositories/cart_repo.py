from typing import List, Dict, Type
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
	async def get_cart (self, cart_id: int, db: AsyncSession) -> Type[Cart] | None:
		pass

	@abstractmethod
	async def save_cart (self, customer_id: int, db: AsyncSession, details: List[CartDetail] | None) -> Type[Cart]:
		pass

	@abstractmethod
	async def delete_cart (self, cart_id: int, db: AsyncSession) -> Dict[str, str]:
		pass

	@abstractmethod
	async def update_cart (self, cart: Cart, product_id: int, new_quatity: int, db: AsyncSession) -> Cart | None:
		pass

class CartRepository (CartAbstraction):
	@classmethod
	async def get_cart (cls, cart_id: int, db: AsyncSession) -> Type[Cart] | None:
		cart = await db.get(entity=Cart,ident=cart_id)
		if not cart:
			return None
		return cart

	@classmethod
	async def save_cart (cls, customer_id: int, db: AsyncSession, details: List[CartDetail] | None) -> Cart:
		if details is None:
			raise ValueError ("At least one product should be selected!!!") ### replace with class of errors

		try:
			new_cart = Cart (customer_id=customer_id, updated_at=func.now (), details=details)
			db.add (new_cart)
			await db.commit ()  ##### remove it later service logic based from Medium Article
			return new_cart
		except BaseException as e:
			return {"DB_CART": f"Error from db as {e}"}  ### replace with class of errors

	@classmethod
	async def delete_cart (cls, cart: Cart, db: AsyncSession) ->  None:
		if cart is None:
			return None
		await db.delete(cart)
		await db.commit ()  ##### remove it later service logic based from Medium Article
		return {"DB_CART": f"Cart with id {Cart.id} was deleted from DB"}  ### replace with class of errors

	@classmethod
	async def update_cart (cls, cart: Type[Cart], product_id: int, new_quatity: int, db: AsyncSession) -> Dict[str, str] | None:
		if cart is None:
			return None

		pointer = next((k for k in cart.details if k.product_id == product_id), None)
		if pointer is None:
			raise ValueError (f"There is no product_id {product_id} in CartDetail!!!")

		cart.updated_at = func.now ()
		pointer.quantity = new_quatity
		await db.commit ()  ##### remove it later service logic based from Medium Article
		return {"DB_CART": f"Cart with id {29}, was successfully updated"}  ### replace with class of errors

async def main ():
	async with session_manager.session () as db:
		# await CartRepository.save_cart (customer_id=1, db=db, details=[CartDetail (product_id=86, quantity=900), CartDetail (product_id=87,
		#                                                                                                                        quantity=700)])  #
		get_cart= await CartRepository.get_cart (cart_id=7, db=db)

		await CartRepository.update_cart (cart=get_cart, product_id=5, new_quatity=333333, db=db)
		# print(await CartRepository.delete_cart(cart=get_cart, db=db))

asyncio.run (main ())
