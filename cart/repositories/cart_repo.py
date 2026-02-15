from abc import ABC, abstractmethod
from cart.models.cart import Cart

class OrderAbstraction (ABC):
	@abstractmethod
	async def get_cart (self, curt_id: int)-> Cart:
		pass

	@abstractmethod
	async def create_cart (self, curt_id: int)-> Cart:
		pass

	@abstractmethod
	async def delete_cart (self, curt_id: int)-> Cart[int]:
		pass

	@abstractmethod
	async def update_cart(self, curt_id)-> Cart:
		pass
