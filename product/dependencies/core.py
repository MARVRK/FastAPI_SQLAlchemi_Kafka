from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from product.infra.base import get_db
from product.repositories.product_repo import ProductRepository
from product.services.product_service import ProductService


def get_product_service(db: AsyncSession = Depends(get_db)) -> ProductService:
    repo = ProductRepository()
    return ProductService(repo=repo, db=db)


ProductServiceDep = Annotated[ProductService, Depends(get_product_service)]
