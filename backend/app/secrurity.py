from typing import Optional
from datetime import datetime, timedelta

from jose import jwt

from app.config import config

ALG = 'HS256'


class TokenFunc():
    def create_access_token(
        self,
        exp_delta: timedelta = None
    ) -> str:
        if exp_delta:
            exp = datetime.utcnow() + exp_delta
        else:
            exp = datetime.utcnow() + timedelta(
                hours = config.ACCESS_TOKEN_EXP_HOURS
            )
        payload = {'exp': exp, 'iss': 'debug'}
        encoded_jwt = jwt.encode(payload, config.SECRET_KEY, algorithm=ALG)
        return encoded_jwt


tokenfunc = TokenFunc()
