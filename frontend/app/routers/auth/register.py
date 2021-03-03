from fastapi import APIRouter

from app import schema
from app.api import authfunc
from app.login.func import secret_required


router = APIRouter()

@router.on_event('startup')
async def register_startup():
    # for unknown reason, logger do not work on connect startup
    ...

@router.post('/register')
@secret_required
async def register(
    user_in: schema.UserRegister,
    secret: schema.Secret
):
    jwt: schema.JWT = await authfunc.register(user_in.name, user_in.email, user_in.password)
    payload = await authfunc.retrieve_payload(jwt.access_token)
    return payload
