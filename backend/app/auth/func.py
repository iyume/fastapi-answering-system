from typing import Optional

from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm.session import Session

from app import crud
from app.config import config
from app.auth.deps import get_db
from app.security.jwt import ALG

pwd_cryptor = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(plain_pwd: str, hashed_pwd: Optional[str]) -> bool:
    return pwd_cryptor.verify(plain_pwd, hashed_pwd)

def encrypt_password(pwd: str) -> str:
    return pwd_cryptor.encrypt(pwd)

def validate(name: str, plain_pwd: str):
    db: Session = next(get_db())
    hashed_pwd = crud.user.get_by_name(db, name)
    db.close()
    is_valid = verify_password(plain_pwd, hashed_pwd)
    return is_valid

def jwt_decode(token: str):
    payload = jwt.decode(
        token, config.SECRET_KEY, algorithms=ALG
    )
    return {**payload}
