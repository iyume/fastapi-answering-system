from typing import Optional

from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserPayload(BaseModel):
    id: str
    name :str
    email: EmailStr
    exp: int
    is_active: bool
    is_superuser: bool


class UserDetail(BaseModel):
    id: str
    name: str
    email: EmailStr
    wechat: Optional[str] = None
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False
    created_time: int
    first_login: Optional[str] = None
