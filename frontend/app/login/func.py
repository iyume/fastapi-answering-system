from typing import Any
from functools import wraps

from fastapi.responses import RedirectResponse, PlainTextResponse

from app.config import super_secret, logger


def login_required(func: Any) -> Any:
    @wraps(func)
    async def wrapper(**kwds: Any) -> Any:
        if 'current_user' not in kwds:
            return await func(**kwds)
        if not getattr(kwds['current_user'], 'is_authenticated', None):
            return RedirectResponse(kwds['request'].url_for('login'))
        return await func(**kwds)
    return wrapper


def secret_required(func: Any) -> Any:
    @wraps(func)
    async def wrapper(**kwds: Any) -> Any:
        if 'secret' not in kwds:
            return PlainTextResponse('Secret required', status_code=403)
        if kwds['secret'].secret != super_secret:
            logger.warning(f'[Info] Secret is {super_secret}\n')
            return PlainTextResponse('Secret wrong', status_code=403)
        return await func(**kwds)
    return wrapper
