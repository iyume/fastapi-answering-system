from fastapi import Cookie

from app.api import authfunc
from app.models.subject import subjects, Subjects
from app.models.user import UserPayload


def get_subjects() -> Subjects:
    return subjects

async def get_current_user(jwt: str = Cookie(None)) -> UserPayload:
    if not jwt:
        return UserPayload(None)
    user_dict = await authfunc.retrieve_payload(jwt)
    if not user_dict:
        return UserPayload(None)
    return UserPayload(user_dict)
