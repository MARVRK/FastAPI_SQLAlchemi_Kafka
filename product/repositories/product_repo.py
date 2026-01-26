from abc import ABC, abstractmethod
from typing import Dict

from product.models.product import Product

class ProductAbstraction (ABC):
	@abstractmethod
	def get_product (self, product_id: int)-> Product :
		pass

	@abstractmethod
	def create_product (self, product_name: str)-> Product:
		pass

	@abstractmethod
	def delete_product (self, product_id: int)-> Dict[str, int]:
		pass

	@abstractmethod
	def update_product (self, product_id: int)-> Product:
		pass
