from typing import List

from fastapi import Cookie

from app.models.subject import subjects, Subjects


def get_subjects() -> Subjects:
    return subjects

def get_current_user(jwt: str = Cookie(None)):
    ...
