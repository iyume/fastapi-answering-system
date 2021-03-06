from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from app import schema, crud
from app.auth import deps, func
from app.security import jwt
from app.models.user import User


router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/access-token')
async def access_token(
    user_in: schema.UserAuth
) -> Any:
    user = User(user_in.name, user_in.password)
    if not user.is_authenticated:
        return 'incorrect name or password'
    if not user.is_active:
        return 'inactive user'
    token = jwt.create_access_token(
        schema.UserJWT(
            id = user.id,
            iss = user.name,
            email = user.email,
            is_active = user.is_active,
            is_superuser = user.is_superuser
        )
    )
    return {"access-token": token}


@router.post('/retrieve-payload')
async def retrive_payload(obj_in: schema.JWTStr) -> Any:
    """
    post jwt and response jwt_decoded (also for validate)
    """
    payload = schema.UserJWT(**func.jwt_decode(obj_in.jwt))
    return payload

@router.post('/retrieve-resume')
async def retrieve_resume(
    obj_in: schema.JWTStr,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    post jwt and response user detail
    """
    payload = schema.UserJWT(**func.jwt_decode(obj_in.jwt))
    user = crud.user.get_by_id(db, payload.id)
    return user

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
) -> Any:
    if crud.user.get_by_email(db, user_in.email) or crud.user.get_by_name(db, user_in.name):
        return 'existed email or name'
    user = crud.user.create(db, user_in, is_superuser=False)
    return user

@router.post('/drop-user')
async def drop_user(
    name: str,
    db: Session = Depends(deps.get_db)
) -> Any:
    if crud.user.get_by_name(db, name):
        return crud.user.drop(db, name)
    return 'no such user'
