from typing import Optional

from pydantic import BaseModel, EmailStr


class UserAuth(BaseModel):
    name: str
    password: str


class UserChangePassword(BaseModel):
    uid: str
    password_new: str


class UserBase(BaseModel):
    is_active: bool = True
    is_superuser: bool = False

class UserJWT(UserBase):
    uid: str
    iss: str
    email: EmailStr
    exp: Optional[float]

class UserCreate(UserBase):
    name: str
    email: Optional[EmailStr] = None
    password: str
    hashed_password: Optional[str] = None

