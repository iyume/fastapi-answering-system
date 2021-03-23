from typing import Optional
from passlib.context import CryptContext

from jose import jwt
from fastapi import HTTPException
from sqlalchemy.orm.session import Session

from app import crud
from app.config import config
from . import deps
from app.security.jwt import ALG

pwd_cryptor = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(plain_pwd: str, hashed_pwd: str) -> bool:
    return pwd_cryptor.verify(plain_pwd, hashed_pwd)

def encrypt_password(pwd: str) -> str:
    return pwd_cryptor.encrypt(pwd)

def validate(name: str, password: str) -> bool:
    db: Session = next(deps.get_db())
    user = crud.user.get_by_name(db, name)
    db.close()
    if not user:
        return False
    return verify_password(password, user.hashed_password)

def jwt_decode(token: str) -> dict:
    try:
        payload = jwt.decode(
            token, config.SECRET_KEY, algorithms=ALG
        )
    except jwt.JWTError:
        raise HTTPException(status_code=403, detail='Could not validate json web token')
    return {**payload}
