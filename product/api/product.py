from typing import List

from fastapi import APIRouter

from product.dependencies.core import ProductServiceDep
from product.schemas.requests import ProductCreate, ProductUpdate
from product.schemas.responses import ProductResponse

router = APIRouter(prefix="/product")


@router.get("/", response_model=List[ProductResponse])
async def get_all_products(service: ProductServiceDep):
    return await service.get_all_products()


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, service: ProductServiceDep):
    return await service.get_product(product_id)


@router.post("/", response_model=ProductResponse, status_code=201)
async def create_product(data: ProductCreate, service: ProductServiceDep):
    return await service.create_product(data)


@router.patch("/{product_id}", response_model=ProductResponse)
async def update_product(product_id: int, data: ProductUpdate, service: ProductServiceDep):
    return await service.update_product(product_id, data)


@router.delete("/{product_id}", status_code=200)
async def delete_product(product_id: int, service: ProductServiceDep):
    return await service.delete_product(product_id)
