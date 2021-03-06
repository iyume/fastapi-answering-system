from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserPayload(BaseModel):
    name :str
    email: EmailStr
    exp: int
    is_active: bool
    is_superuser: bool
    is_authenticated: bool
