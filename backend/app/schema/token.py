from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str

class JWTStr(BaseModel):
    jwt: str
