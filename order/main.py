import sys
from order.error.error import ServiceUnavailable
from order.api.order import router as order_router
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from loguru import logger



app = FastAPI()
app.include_router(router=order_router)

@app.exception_handler(ServiceUnavailable)
async def service_error(request: Request, exc: ServiceUnavailable):
    return JSONResponse(status_code=503, content={"status": "error", "code": exc.code, "service": exc.service, "message":exc.message})

@app.exception_handler(IntegrityError)
async def handler_integrity_error(request: Request, exc: IntegrityError):
    return JSONResponse(status_code=500, content={"status": "error", "code":"DB_CONFLICT", "message": "conflict"})

@app.exception_handler(SQLAlchemyError)
async def handler_database_error(request: Request, exc: SQLAlchemyError):
    return JSONResponse(status_code=500, content={"status": "error", "code":"DB_ERROR","message": "internal_error"})
