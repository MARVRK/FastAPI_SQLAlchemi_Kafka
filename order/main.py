from api.order import router as order_router
from fastapi import FastAPI

app = FastAPI()
app.include_router(router=order_router)


