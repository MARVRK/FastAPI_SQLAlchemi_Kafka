from fastapi import APIRouter

router = APIRouter(prefix="/order")

@router.get("/")
async def check_health_order():
	return {"order_health" : "Status OK"}