from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from product.infra.base import get_db
from product.schemas import ProductCreate, ProductUpdate, ProductResponse
from product.services import product_service

router = APIRouter(prefix="/product")

DBSessionDP = Annotated[AsyncSession, Depends(get_db)]


@router.get("/", response_model=List[ProductResponse])
async def get_all_products(db: DBSessionDP):
    return await product_service.get_all_products(db)


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: DBSessionDP):
    return await product_service.get_product(product_id, db)


@router.post("/", response_model=ProductResponse, status_code=201)
async def create_product(data: ProductCreate, db: DBSessionDP):
    return await product_service.create_product(data, db)


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(product_id: int, data: ProductUpdate, db: DBSessionDP):
    return await product_service.update_product(product_id, data, db)


@router.delete("/{product_id}")
async def delete_product(product_id: int, db: DBSessionDP):
    return await product_service.delete_product(product_id, db)
