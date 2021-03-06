from typing import Optional

from pydantic import BaseModel, EmailStr


class UserAuth(BaseModel):
    name: str
    password: str


class UserBase(BaseModel):
    is_active: bool = True
    is_superuser: bool = False

class UserJWT(UserBase):
    id: str
    iss: str
    email: EmailStr
    exp: Optional[str]

class UserCreate(UserBase):
    name: str
    email: EmailStr
    password: str

