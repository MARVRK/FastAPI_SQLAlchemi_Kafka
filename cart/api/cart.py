from fastapi import APIRouter

router = APIRouter(prefix="/cart")

@router.get("/")
async def check_health_order():
	return {"cart_health" : "Status OK"}