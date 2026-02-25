from abc import ABC, abstractmethod
from typing import Dict

from product.models.product import Product

class ProductAbstraction (ABC):
	@abstractmethod
	async def get_product (self, product_id: int)-> Product :
		pass

	@abstractmethod
	async def create_product (self, product_name: str)-> Product:
		pass

	@abstractmethod
	async def delete_product (self, product_id: int)-> Dict[str, int]:
		pass

	@abstractmethod
	async def update_product (self, product_id: int)-> Product:
		pass
