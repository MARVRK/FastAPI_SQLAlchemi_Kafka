from fastapi import APIRouter

router = APIRouter(prefix="/product")

@router.get("/")
async def check_health_product():
	return {"product_health" : "Status OK"}