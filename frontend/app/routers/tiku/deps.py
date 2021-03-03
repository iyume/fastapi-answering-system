from fastapi import Cookie

from app.api import authfunc
from app.models.subject import subjects, Subjects
from app.models.user import User


def get_subjects() -> Subjects:
    return subjects

async def get_current_user(jwt: str = Cookie(None)) -> User:
    if not jwt:
        return User(None)
    user_dict = await authfunc.retrieve_user(jwt)
    if not user_dict:
        return User(None)
    return User(user_dict)
