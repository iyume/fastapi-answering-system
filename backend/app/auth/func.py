from typing import Optional

from passlib.context import CryptContext
from sqlalchemy.orm.session import Session

from app import crud
from app.auth.deps import get_db
from app.models.user import User

pwd_cryptor = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(plain_pwd: str, hashed_pwd: Optional[str]) -> bool:
    return pwd_cryptor.verify(plain_pwd, hashed_pwd)

def encrypt_password(pwd: str) -> str:
    return pwd_cryptor.encrypt(pwd)

def validate(name: str, plain_pwd: str) -> bool:
    if user := User(name):
        hashed_password = user.hashed_password
        is_valid = verify_password(plain_pwd, hashed_password)
        return is_valid
    else:
        return False
