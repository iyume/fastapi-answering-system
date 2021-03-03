import secrets
from typing import Optional
from pydantic import EmailStr

from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from app.api import authfunc
from app.schema import Token, UserRegister, Secret
from app.login.func import secret_required


router = APIRouter()

@router.on_event('startup')
async def register_startup():
    # for unknown reason, logger do not work on connect startup
    ...

@router.post('/register')
@secret_required
async def register(
    user_in: UserRegister,
    secret: Secret
):
    content = await authfunc.register(user_in.name, user_in.email, user_in.password)
    if isinstance(content, str):
        return content
    if isinstance(content, Token):
        return content.access_token
    raise HTTPException(status_code=500, detail='Unknown error')
