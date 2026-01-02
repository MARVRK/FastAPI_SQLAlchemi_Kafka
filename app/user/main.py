from fastapi import FastAPI
from app.user.api.user import router as user_router
app = FastAPI()
app.include_router(router=user_router)