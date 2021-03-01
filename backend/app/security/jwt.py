from typing import Optional
from datetime import datetime, timedelta

from jose import jwt

from app.config import config
from app.schema.user import UserJWT


ALG = 'HS256'    

def create_access_token(
    user: UserJWT,
    exp_hours: int = None
) -> str:
    exp = datetime.utcnow() + timedelta(
        hours = exp_hours or config.ACCESS_TOKEN_EXP_HOURS
    )
    payload = {
        'iss': user.name,
        'email': user.email,
        'exp': exp
    }
    encoded_jwt = jwt.encode(payload, config.SECRET_KEY, algorithm=ALG)
    return encoded_jwt
