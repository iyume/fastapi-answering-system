from typing import Any
import time
from functools import wraps
from inspect import iscoroutinefunction

from fastapi.responses import RedirectResponse, PlainTextResponse
from fastapi.exceptions import HTTPException

from app.config import super_secret, logger


def login_required(func: Any) -> Any:
    @wraps(func)
    async def wrapper(**kwargs: Any) -> Any:
        if 'current_user' not in kwargs:
            return RedirectResponse(kwargs['request'].url_for('login'))
        if not getattr(kwargs['current_user'], 'is_authenticated', None):
            return RedirectResponse(kwargs['request'].url_for('login'))
        if getattr(kwargs['current_user'], 'exp') < time.time():
            rr = RedirectResponse(kwargs['request'].url_for('login'))
            rr.set_cookie('jwt', value='delete', expires=0)
            return rr
        if iscoroutinefunction(func):
            return await func(**kwargs)
        else:
            return func(**kwargs)
    return wrapper


def secret_required(func: Any) -> Any:
    @wraps(func)
    async def wrapper(**kwargs: Any) -> Any:
        if 'secret' not in kwargs:
            return PlainTextResponse('Secret required', status_code=400)
        if kwargs['secret'].secret != super_secret:
            logger.warning(f'Secret is {super_secret}')
            return PlainTextResponse('Secret wrong', status_code=403)
        if iscoroutinefunction(func):
            return await func(**kwargs)
        else:
            return func(**kwargs)
    return wrapper


def superuser_required(func: Any) -> Any:
    @wraps(func)
    async def wrapper(**kwargs: Any) -> Any:
        if 'current_user' not in kwargs:
            return HTTPException(status_code=403)
        if not getattr(kwargs['current_user'], 'is_superuser', None):
            return HTTPException(status_code=403)
        if iscoroutinefunction(func):
            return await func(**kwargs)
        else:
            return func(**kwargs)
    return wrapper
