import jwt
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from user.api.user import router as user_router
from user.error.error import UserError, AuthError

app = FastAPI()
app.include_router(router=user_router)


@app.exception_handler(UserError)
async def handler_user_error(request: Request, exc: UserError):
    return JSONResponse(status_code=404, content={"status": "error", "message": str(exc)})


@app.exception_handler(AuthError)
async def handler_auth_error(request: Request, exc: AuthError):
    return JSONResponse(status_code=401, content={"status": "error", "message": str(exc)})


@app.exception_handler(IntegrityError)
async def handler_integrity_error(request: Request, exc: IntegrityError):
    return JSONResponse(status_code=409, content={"status": "error", "message": "user with this email already exists"})


@app.exception_handler(jwt.ExpiredSignatureError)
async def handler_token_expired(request: Request, exc: jwt.ExpiredSignatureError):
    return JSONResponse(status_code=401, content={"status": "error", "message": "token expired"})


@app.exception_handler(jwt.InvalidTokenError)
async def handler_invalid_token(request: Request, exc: jwt.InvalidTokenError):
    return JSONResponse(status_code=401, content={"status": "error", "message": "invalid token"})
