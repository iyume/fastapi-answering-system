import secrets
from typing import Optional
import logging

from fastapi import APIRouter

from app.api import authfunc
from app.schema import Token


logger = logging.getLogger('fastapi')
super_token = secrets.token_urlsafe(32)


router = APIRouter()

@router.on_event('startup')
async def register_startup():
    # for unknown reason, logger do not work on connect startup
    ...

@router.post('/register')
async def register(
    name: str,
    email: str,
    password: str,
    token: Optional[str] = None
):
    if not token:
        return 'token required'
    if token != super_token:
        logger.warning(f'Secret is { super_token }')
        return 'token wrong'
    content = await authfunc.register(name, email, password)
    if isinstance(content, str):
        return content
    if isinstance(content, Token):
        return content.access_token
    return 'Unknown error'
