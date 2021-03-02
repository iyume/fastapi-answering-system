from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    is_active: bool = True
    is_superuser: bool = False

class UserJWT(UserBase):
    iss: str
    email: EmailStr
    exp: int

class UserCreate(UserBase):
    name: str
    email: EmailStr
    password: str

class UserDrop(UserBase):
    name: str
