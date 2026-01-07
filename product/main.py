from fastapi import FastAPI
from api.product import router as product_router

app = FastAPI()
app.include_router(router=product_router)