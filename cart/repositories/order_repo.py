from abc import ABC, abstractmethod
from typing import Dict
from order.models.order import Order

class OrderAbstraction (ABC):
	@abstractmethod
	async def get_order (self, order_id: int)-> Order:
		pass

	@abstractmethod
	async def create_order (self, user_id: int)-> Order:
		pass
	# должен ли юзер писать вручную свой ади или при создании заказа автоматом подтягивать с базы адишник, поскольку нужно пройти авторизацию

	@abstractmethod
	async def delete_order(self, order_id: int)-> Dict[str, int]:
		pass

	@abstractmethod
	async def update_order(self, order_id)-> Order:
		pass
