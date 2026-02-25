from fastapi import APIRouter

router = APIRouter(prefix="/user")

@router.get("/")
async def check_health_user():
	return {"User_Health":"Status OK"}