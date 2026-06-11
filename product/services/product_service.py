from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from product.error.error import ProductError
from product.models.product import Product
from product.repositories.product_repo import ProductRepository
from product.schemas.requests import ProductCreate, ProductUpdate
from product.schemas.responses import ProductResponse


class ProductService:
    def __init__(self, repo: ProductRepository, db: AsyncSession):
        self.repo = repo
        self.db = db

    async def get_product(self, product_id: int) -> ProductResponse:
        product = await self.repo.get_product(product_id, self.db)
        if not product:
            raise ProductError(f"Product with id {product_id} not found")
        return ProductResponse.model_validate(product)

    async def get_all_products(self) -> List[ProductResponse]:
        products = await self.repo.get_all_products(self.db)
        return [ProductResponse.model_validate(p) for p in products]

    async def create_product(self, data: ProductCreate) -> ProductResponse:
        product = Product(product=data.product, available_amount=data.available_amount)
        created = await self.repo.create_product(product, self.db)
        await self.db.commit()
        return ProductResponse.model_validate(created)

    async def update_product(self, product_id: int, data: ProductUpdate) -> ProductResponse:
        updated = await self.repo.update_product(product_id, data.model_dump(exclude_none=True), self.db)
        if not updated:
            raise ProductError(f"Product with id {product_id} not found")
        await self.db.commit()
        return ProductResponse.model_validate(updated)

    async def delete_product(self, product_id: int) -> int:
        product = await self.repo.get_product(product_id, self.db)
        if not product:
            raise ProductError(f"Product with id {product_id} not found")
        result = await self.repo.delete_product(product_id, self.db)
        await self.db.commit()
        return result
