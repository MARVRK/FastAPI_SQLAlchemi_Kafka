from abc import ABC, abstractmethod
from typing import List

from sqlalchemy import select, delete, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from product.models.product import Product


class ProductAbstraction(ABC):
    @abstractmethod
    async def get_product(self, product_id: int, db: AsyncSession) -> Product | None:
        pass

    @abstractmethod
    async def get_all_products(self, db: AsyncSession) -> List[Product]:
        pass

    @abstractmethod
    async def create_product(self, product: Product, db: AsyncSession) -> Product:
        pass

    @abstractmethod
    async def update_product(self, product_id: int, data: dict, db: AsyncSession) -> Product | None:
        pass

    @abstractmethod
    async def delete_product(self, product_id: int, db: AsyncSession) -> int:
        pass


class ProductRepository(ProductAbstraction):
    async def get_product(self, product_id: int, db: AsyncSession) -> Product | None:
        result = await db.execute(select(Product).where(Product.id == product_id))
        return result.scalar_one_or_none()

    async def get_all_products(self, db: AsyncSession) -> List[Product]:
        result = await db.execute(select(Product))
        return list(result.scalars().all())

    async def create_product(self, product: Product, db: AsyncSession) -> Product:
        stmt = (
            insert(Product)
            .values(product=product.product, available_amount=product.available_amount)
            .returning(Product)
        )
        result = await db.execute(stmt)
        return result.scalar_one()

    async def update_product(self, product_id: int, data: dict, db: AsyncSession) -> Product | None:
        stmt = (
            update(Product)
            .where(Product.id == product_id)
            .values(**data)
            .returning(Product)
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def delete_product(self, product_id: int, db: AsyncSession) -> int:
        await db.execute(delete(Product).where(Product.id == product_id))
        return product_id
