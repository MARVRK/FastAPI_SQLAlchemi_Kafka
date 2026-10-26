from uuid import UUID
from abc import ABC, abstractmethod
from order.models.order import Order, ProductsInOrder
from sqlalchemy.ext.asyncio import AsyncSession
from order.domain.entities import PlacedOrder
from sqlalchemy.exc import IntegrityError
from sqlalchemy.dialects.postgresql import insert

from order.error.error import OrderError
from loguru import logger

# logger.add(sys.stdout, level="DEBUG", format="<green>{time:HH:mm:ss}</green> | {level} | {message}")
# logger.add("order_repo.log", serialize=True, level="INFO")
# logger.add("errors.log", level="ERROR")

class OrderAbstraction (ABC):

    @abstractmethod
    async def create_order (self, new_order: PlacedOrder, db: AsyncSession) -> PlacedOrder:
        pass

    @abstractmethod
    async def cancel_order (self, user_id: int, order_number: UUID, db: AsyncSession) -> PlacedOrder | None:
        pass

    @abstractmethod
    async def get_one_order (self, user_id: int, order_number: UUID, db: AsyncSession) -> PlacedOrder | None:
        pass

    @abstractmethod
    async def get_orders (self, user_id: int, db: AsyncSession) -> list[PlacedOrder]:
        pass

# class OrderRepository (OrderAbstraction):
# 		pass