from typing import Optional
from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from app.config import config


pwd_cryptor = CryptContext(schemes=['bcrypt'], deprecated='auto')


class TokenFunc():
    alg = 'HS256'    

    def create_access_token(
        self,
        exp_hours: int = None
    ) -> str:
        exp = datetime.utcnow() + timedelta(
            hours = exp_hours or config.ACCESS_TOKEN_EXP_HOURS
        )
        payload = {'exp': exp, 'iss': 'debug'}
        encoded_jwt = jwt.encode(payload, config.SECRET_KEY, algorithm=self.alg)
        return encoded_jwt

    def verify_password(self, plain_pwd: str, hashed_pwd: str):
        return pwd_cryptor.verify(plain_pwd, hashed_pwd)

    def encrypt_password(self, pwd: str) -> str:
        return pwd_cryptor.encrypt(pwd)


tokenfunc = TokenFunc()
