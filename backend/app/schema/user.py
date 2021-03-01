from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    is_active: bool = True
    is_superuser: bool = False

class UserJWT(BaseModel):
    name: str
    email: EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
