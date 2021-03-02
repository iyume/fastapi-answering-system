from typing import Optional

from fastapi import APIRouter, Depends

from sqlalchemy.orm.session import Session

from app import schema, crud
from app.auth import deps, func
from app.security import jwt
from app.models.user import User

router = APIRouter(prefix='/auth', tags=['auth'])

@router.post('/access-token')
async def access_token(
    name: str,
    password: str
):
    user = User(name, password)
    if user.is_authenticated:
        if not user.is_active:
            return 'inactive user'
        token = jwt.create_access_token(
            schema.UserJWT(
                name = user.name,
                email = user.email,
                is_superuser = user.is_superuser
            )
        )
        return {
            "access-token": token
        }
    return 'incorrect name or password'

@router.post('/retrieve-user')
async def retrive_user(obj_in: schema.JWTStr):
    payload = schema.UserJWT(**func.jwt_decode(obj_in.jwt))
    user = User(payload.iss)
    if user.is_active:
        return user.current_user
    else:
        return 'inactive user'

# @router.post('/refresh-token')
# async def refresh_token():
#     ...

# @router.post('/revoke-access')
# async def revoke_access():
#     ...

# @router.post('/revoke-refresh')
# async def revoke_refresh():
#     ...

@router.post('/register')
async def register(
    user_in: schema.UserCreate,
    db: Session = Depends(deps.get_db)
):
    if crud.user.get_by_email(db, user_in.email) or crud.user.get_by_name(db, user_in.name):
        return 'existed email or name'
    user = crud.user.create(db, user_in, is_superuser=False)
    return user

@router.post('/drop-user')
async def drop_user(
    name: str,
    db: Session = Depends(deps.get_db)
):
    if crud.user.get_by_name(db, name):
        return crud.user.drop(db, name)
    return 'no such user'
