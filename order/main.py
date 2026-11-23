import sys
from order.error.error import ServiceUnavailable
from order.api.order import router as order_router
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from loguru import logger

logger.remove()
logger.add(sys.stderr, backtrace=True, enqueue=True)

app = FastAPI()
app.include_router(router=order_router)

@app.exception_handler(ServiceUnavailable)
async def service_error(request: Request, exc: ServiceUnavailable):
    logger.warning("Order_Service_Error, service: {service}, method: {method}, path:{path}",
                   service = exc.service,
                   method=request.method,
                   path=request.url.path)
    return JSONResponse(status_code=503, content={"status": "error","service" : exc.service, "code": exc.code, "message":exc.message})

@app.exception_handler(IntegrityError)
async def handler_integrity_error(request: Request, exc: IntegrityError):
    logger.opt(exception=exc).error("ORDER_DB_Integrity_Error method: {method}", method=request.method)
    return JSONResponse(status_code=500, content={"status": "error", "code":"DB_CONFLICT", "message": "conflict"})

@app.exception_handler(SQLAlchemyError)
async def handler_database_error(request: Request, exc: SQLAlchemyError):
    logger.opt(exception=exc).error("ORDER_DB_Sqlalchemy_Error method: {method}", method=request.method)
    return JSONResponse(status_code=500, content={"status": "error", "code":"DB_ERROR", "message": "internal_error"})
