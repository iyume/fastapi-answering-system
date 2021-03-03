from functools import wraps

from fastapi.responses import RedirectResponse


def login_required(func):
    @wraps(func)
    async def wrapper(**kwds):
        if not getattr(kwds['current_user'], 'is_authenticated', None):
            return RedirectResponse(kwds['request'].url_for('login'))
        return await func(**kwds)
    return wrapper
