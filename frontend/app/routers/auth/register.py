import secrets

from fastapi import APIRouter
from starlette.requests import Request

from app.api import authfunc


router = APIRouter()

@router.post('/register')
async def register(
    request: Request,
    name: str,
    email: str,
    password: str
):
    content = await authfunc.register(name, email, password)
    return content
