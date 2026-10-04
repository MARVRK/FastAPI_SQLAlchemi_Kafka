from fastapi import APIRouter, Header
from fastapi.responses import Response
from cart.schemas.responses import CartResponse
from cart.schemas.requests import  CartCreateUpdate
from cart.dependencies.core import CartServiceDep

router = APIRouter (prefix="/cart")

@router.get ("/health")
async def check_health_order ():
    return {"cart_health": "Status OK"}

@router.put ("/", response_model=CartResponse, status_code=200)
async def new_update_cart (service: CartServiceDep, body: CartCreateUpdate, user_id: int = Header (alias="X-User-ID")):
    return await service.create_replace_cart (customer_id=user_id, items=body.items)

@router.delete ("/", response_model=CartResponse, status_code=200)
async def remove_cart (service: CartServiceDep, user_id: int = Header (alias="X-User-ID")):
    result = await service.delete_cart (customer_id=user_id)
    if not result:
        return Response (status_code=204)
    return CartResponse(id=None,items=[])

@router.get ("/", response_model=CartResponse, status_code=200)
async def fetch_cart (service: CartServiceDep, user_id: int = Header (alias="X-User-ID")):
    return await service.get_cart (customer_id=user_id)
