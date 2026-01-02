from fastapi import FastAPI
from app.product.api.product import router as product_router

app = FastAPI()
app.include_router(router=product_router)