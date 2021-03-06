from typing import Optional

from fastapi import Cookie

from app.api import authfunc
from app.models.subject import subjects, Subjects
from app.models.user import UserPayload


def get_subjects() -> Subjects:
    return subjects

async def get_current_user(jwt: str = Cookie(None)) -> Optional[UserPayload]:
    if not jwt:
        return None
    user_dict = await authfunc.retrieve_payload(jwt)
    if not user_dict:
        return None
    return UserPayload(user_dict)
