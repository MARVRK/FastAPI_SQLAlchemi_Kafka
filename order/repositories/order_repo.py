import asyncio
import sys
import uuid
from abc import ABC, abstractmethod
from order.models.order import Order, ProductsInOrder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from sqlalchemy.dialects.postgresql import insert
from order.infra.base import session_manager
from order.error.error import OrderError
from loguru import logger

logger.add(sys.stdout, level="DEBUG", format="<green>{time:HH:mm:ss}</green> | {level} | {message}")
logger.add("order_repo.log", serialize=True, level="INFO")
logger.add("errors.log", level="ERROR")

class OrderAbstraction (ABC):
	@abstractmethod
	async def get_order (self, order_number: uuid, db: AsyncSession)-> Order | None:
		pass

	@abstractmethod
	async def save_update_order (self, order: Order, db: AsyncSession) -> Order.order_number:
		pass

	@abstractmethod
	async def delete_order(self, order: Order, db: AsyncSession)-> dict[str, int] | None:
		pass


class OrderRepository(OrderAbstraction):
	async def get_order(self, order_number: uuid, db: AsyncSession) -> Order | None:
		logger.info (f"Getting order_number from DBOrder: {order_number}")
		if not order_number:
			return None
		result = select(Order).options(selectinload(Order.order_items)).where(Order.order_number == order_number)
		order = await db.execute(result)
		return order.scalar_one_or_none()

	async def save_update_order(self, order: Order, db: AsyncSession) -> Order.order_number:
		if not order.order_items:
			raise OrderError(message="At least one product should be added")

		try:
			logger.info (f"Starting updating/creating a new order_number: {order.order_number}")
			order_stmt = insert(Order).values(order_number=order.order_number,
			                                  status=order.status,
			                                  total_price=order.total_price,
			                                  user_id=order.user_id)
			order_stmt = order_stmt.on_conflict_do_update(constraint="order_order_number",
			                                              set_=dict(order_number=order.order_number,
			                                                        total_price=order.total_price,
			                                                        status=order.status)).returning(Order.id)
			order_execution = await db.execute(order_stmt)
			returned_order_id = order_execution.scalar_one_or_none()


			products_in_order =[{"order_id": returned_order_id,
								 "product_id": d.product_id,
								 "quantity": d.quantity,
								 "price_at_time":d.price_at_time} for d in order.order_items]

			data_stmt = insert(ProductsInOrder).values(products_in_order)
			data_stmt= data_stmt.on_conflict_do_update(constraint="products_in_order_id_product_id",
			                                           set_=dict(quantity=data_stmt.excluded.quantity,
			                                                     price_at_time=data_stmt.excluded.price_at_time))
			await db.execute(data_stmt)
			return order.order_number
		except IntegrityError as error:
			logger.error("Failed to update/create new order")
			raise OrderError(f"Failed to save/update order", original_exception=error)


	async def delete_order(self, order: Order, db: AsyncSession) -> dict[str, str] | None:
		logger.info (f"Deleting order from DBOrder: {order.order_number}")
		if order is None:
			return None
		order_stmt = delete(Order).where(Order.id == order.id)
		await db.execute(order_stmt)
		return {"DB_ORDER": f"Order with id {order.id} was deleted from DB"}
