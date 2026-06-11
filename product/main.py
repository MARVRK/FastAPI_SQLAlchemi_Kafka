from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from product.api.product import router as product_router
from product.error.error import ProductError

app = FastAPI()
app.include_router(router=product_router)


@app.exception_handler(ProductError)
async def handler_product_error(request: Request, exc: ProductError):
    return JSONResponse(status_code=404, content={"status": "error", "message": str(exc)})


@app.exception_handler(IntegrityError)
async def handler_integrity_error(request: Request, exc: IntegrityError):
    msg = str(exc.orig)
    if "product" in msg:
        message = "product with this name already exists"
    else:
        message = "conflict: duplicate value"
    return JSONResponse(status_code=409, content={"status": "error", "message": message})
