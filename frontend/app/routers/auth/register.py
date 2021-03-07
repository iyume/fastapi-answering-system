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
    content = await authfunc.register(user_in.name, user_in.email, user_in.password)
    if isinstance(content, str):
        return content
    payload = await authfunc.retrieve_payload(content.access_token)
    return payload
