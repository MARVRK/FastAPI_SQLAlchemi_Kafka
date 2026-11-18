from uuid import UUID
from abc import ABC, abstractmethod
from order.models.order import Order, ProductsInOrder
from sqlalchemy.ext.asyncio import AsyncSession
from order.domain.entities import PlacedOrder, ProductsFromOrder
from order.domain.enums import OrderStatus
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, update
from collections import defaultdict


class OrderAbstraction (ABC):

    @abstractmethod
    async def create_order (self, user_id: int, new_order: PlacedOrder, db: AsyncSession) -> None:
        pass

    @abstractmethod
    async def cancel_order (self, user_id: int, order_number: UUID, db: AsyncSession) -> PlacedOrder | None:
        pass

    @abstractmethod
    async def get_one_order (self, user_id: int, order_number: UUID, db: AsyncSession) -> PlacedOrder | None:
        pass

    @abstractmethod
    async def get_orders (self, user_id: int, db: AsyncSession) -> list[PlacedOrder] :
        pass

class OrderRepository (OrderAbstraction):


    async def _fetch_items_from_order(self, order_id: int, db: AsyncSession) -> tuple[ProductsFromOrder,...]:
        product_stmt = select(ProductsInOrder.quantity,
                              ProductsInOrder.price_at_time,
                              ProductsInOrder.product_id).where(ProductsInOrder.order_id == order_id)

        product_entity = await db.execute(product_stmt)
        fetched_products = product_entity.all()

        order_items = tuple(ProductsFromOrder(product_id=row.product_id,
                                              quantity=row.quantity,
                                              price_at_time=row.price_at_time) for row in fetched_products)

        return order_items

    async def create_order (self, user_id: int, new_order: PlacedOrder, db: AsyncSession) -> None:
        order_stmt = insert(Order).values(user_id=user_id,
                                          status=new_order.status,
                                          order_number=new_order.order_number).returning(Order.id)

        executed_order = await db.execute(order_stmt)
        order_id = executed_order.scalar_one()

        order_items = [{"order_id":order_id, "product_id": item.product_id,
                       "quantity": item.quantity,"price_at_time":item.price_at_time} for item in new_order.items]

        items_in_new_order = insert(ProductsInOrder).values(order_items)

        await db.execute(items_in_new_order)
        return None

    async def get_one_order(self, user_id: int, order_number: UUID, db: AsyncSession) -> PlacedOrder | None:
        order_stmt = (select (Order.id, Order.status).where(Order.user_id == user_id).
                                                      where(Order.order_number == order_number))

        order_entity = await db.execute(order_stmt)
        fetched_order = order_entity.one_or_none()

        if fetched_order is None:
            return None

        products_from_order = await self._fetch_items_from_order(order_id=fetched_order.id, db=db)

        return PlacedOrder(order_number=order_number,
                           status=fetched_order.status,
                           items=products_from_order)

    async def cancel_order(self, user_id: int, order_number: UUID, db: AsyncSession) -> PlacedOrder | None :
        update_stmt = (update(Order).where(Order.order_number==order_number)
                       .where(Order.user_id==user_id)
                       .where(Order.status==OrderStatus.CREATED)
                       .values(status=OrderStatus.CANCELLED).returning(Order.id))

        order_entity = await db.execute(update_stmt)
        order_id = order_entity.scalar_one_or_none()

        if order_id is None:
            return None

        products_from_order = await  self._fetch_items_from_order(order_id=order_id, db=db)

        return PlacedOrder(order_number=order_number,status=OrderStatus.CANCELLED,items=products_from_order)

    async def get_orders(self, user_id: int, db: AsyncSession) -> list[PlacedOrder] :
        order_stmt = (select(Order.id, Order.status, Order.order_number).
                      order_by(Order.id).
                      where(Order.user_id == user_id))

        order_entity = await db.execute(order_stmt)
        fetched_orders = order_entity.all()

        if not fetched_orders:
            return []

        order_ids = [row.id for row in fetched_orders]

        product_stmt = (select(ProductsInOrder.product_id,
                              ProductsInOrder.quantity,
                              ProductsInOrder.price_at_time,
                              ProductsInOrder.order_id).
                              where(ProductsInOrder.order_id.in_(order_ids)))

        product_entity = await db.execute(product_stmt)
        fetched_products = product_entity.all()

        items_by_order_id = defaultdict(list)

        for row in fetched_products:
            items_by_order_id[row.order_id].append(ProductsFromOrder(product_id=row.product_id,
                                                                       quantity=row.quantity,
                                                                       price_at_time=row.price_at_time))

        assembled_orders = [PlacedOrder(status=row.status,
                                        order_number=row.order_number,
                                        items=tuple(items_by_order_id[row.id])) for row in fetched_orders]
        return assembled_orders

            











