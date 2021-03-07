from datetime import datetime, timedelta

from jose import jwt

from app.config import config
from app.schema.user import UserJWT


ALG = 'HS256'

def create_access_token(
    user: UserJWT,
    exp_hours: int = None
) -> str:
    if user.exp:
        exp = (datetime.fromtimestamp(user.exp) + timedelta(
            hours = exp_hours or config.ACCESS_TOKEN_EXP_HOURS
        )).timestamp()
    else:
        exp = (datetime.now() + timedelta(
            hours = exp_hours or config.ACCESS_TOKEN_EXP_HOURS
        )).timestamp()
    payload = {
        'id': user.id,
        'iss': user.iss,
        'email': user.email,
        'is_active': int(user.is_active),
        'is_superuser': int(user.is_superuser),
        'exp': exp
    }
    encoded_jwt = jwt.encode(payload, config.SECRET_KEY, algorithm=ALG)
    return encoded_jwt
