from typing import Any, Optional

from fastapi import Cookie

from app.api import authfunc
from app.models.subject import subjects, Subjects
from app.models.user import UserPayload, UserDetail


def get_subjects() -> Subjects:
    return subjects

async def get_current_user(jwt: str = Cookie(None)) -> Optional[UserPayload]:
    if not jwt:
        return None
    user_dict = await authfunc.retrieve_payload(jwt)
    user_dict['exp'] = float(user_dict['exp'])
    if not user_dict:
        return None
    return UserPayload(user_dict)

async def get_current_user_detail(jwt: str = Cookie(None)) -> Any:
    if not jwt:
        return None
    user_dict = await authfunc.retrieve_detail(jwt)
    user_dict = dict(user_dict)
    if not user_dict:
        return None
    return UserDetail(**user_dict)
