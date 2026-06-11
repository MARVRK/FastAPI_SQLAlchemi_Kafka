from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from product.api.product import router as product_router
from product.error.error import ProductError

app = FastAPI()
app.include_router(router=product_router)


@app.exception_handler(ProductError)
async def product_error_handler(request: Request, exc: ProductError):
    return JSONResponse(status_code=404, content={"detail": exc.message})


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    return JSONResponse(status_code=409, content={"detail": "Product already exists"})
