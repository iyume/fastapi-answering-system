import secrets

from fastapi import APIRouter
from starlette.requests import Request

from app.api import authfunc
from app.schema import Token


router = APIRouter()

@router.post('/register')
async def register(
    request: Request,
    name: str,
    email: str,
    password: str
):
    content = await authfunc.register(name, email, password)
    if isinstance(content, str):
        return content
    if isinstance(content, Token):
        return content.access_token
    return 'Unknown error'
