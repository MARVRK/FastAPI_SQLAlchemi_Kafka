from cart.api.cart import router as cart_router
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from cart.error.error import CartError

app = FastAPI()
app.include_router(router=cart_router)

@app.exception_handler(IntegrityError)
async def handler_integrity_error(request: Request, exc: IntegrityError):
    msg = str(exc.orig)
    if "Integrity error" in msg:
        message = "Duplicates or somthing"
    '''add other messages after tests'''
    return JSONResponse(status_code=409,content={"message": "error","content":f"{message}"})


@app.exception_handler(CartError)
async def handler_notfound_error(request:Request, exc:CartError):
    msg = str (exc.message)
    '''add messages after tests'''
    if exc.message == "No customer_id provided":
        return JSONResponse (status_code=400, content={"message": "error","content":f"{msg}"})

