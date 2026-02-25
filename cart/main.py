from api.cart import router as cart_router
from fastapi import FastAPI

app = FastAPI()
app.include_router(router=cart_router)


