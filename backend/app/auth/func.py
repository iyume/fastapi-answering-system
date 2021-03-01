from typing import Optional

from passlib.context import CryptContext

from app import crud
from app.db.load_db import SessionMaker

pwd_cryptor = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(plain_pwd: str, hashed_pwd: Optional[str]) -> bool:
    return pwd_cryptor.verify(plain_pwd, hashed_pwd)

def encrypt_password(pwd: str) -> str:
    return pwd_cryptor.encrypt(pwd)

def validate(name: str, plain_pwd: str):
    db = SessionMaker()
    hashed_pwd = crud.user.get_by_name(db, name)
    db.close()
    return verify_password(plain_pwd, hashed_pwd)
