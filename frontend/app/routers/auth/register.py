from typing import Any

from fastapi import APIRouter

from app import schema
from app.api import authfunc
from app.security import secret_required


router = APIRouter()


@router.get('/register')
async def register() -> Any:
    return '暂不开放注册'


@router.post('/register')
@secret_required
async def register_action(
    user_in: schema.UserRegister,
    secret: schema.Secret
) -> Any:
    jwt: schema.JWT = await authfunc.register(user_in.name, user_in.email, user_in.password)
    payload = await authfunc.retrieve_payload(jwt.access_token)
    return payload
