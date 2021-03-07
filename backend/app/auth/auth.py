from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from app import schema, crud
from app.auth import deps, authfunc
from app.security import jwt
from app.config import config


router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/access-token')
async def access_token(
    user_in: schema.UserAuth,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    validate form, and string should be shown to client
    """
    user = crud.user.get_by_name(db, user_in.name)
    if not user:
        user = crud.user.get_by_email(db, user_in.name)
    if not user or not authfunc.verify_password(user_in.password, user.hashed_password):
        return '用户名 / 邮箱 / 密码错误'
    if not user.is_active:
        return '用户已被禁用'
    if not user.first_login:
        crud.user.update_first_login(db, user.id)
    token = jwt.create_access_token(
        schema.UserJWT(
            id = user.id,
            iss = user.name,
            email = user.email,
            is_active = user.is_active,
            is_superuser = user.is_superuser,
            exp = None
        )
    )
    return {
        "access_token": token,
        "exp": config.ACCESS_TOKEN_EXP_HOURS * 60 * 60
    }


@router.post('/retrieve-payload')
async def retrive_payload(jwt: str) -> Any:
    """
    post jwt and response jwt_decoded (also for validate)
    """
    payload = schema.UserJWT(**authfunc.jwt_decode(jwt))
    return payload


@router.post('/retrieve-detail')
async def retrieve_detail(
    jwt: str,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    post jwt and response user detail
    """
    payload = schema.UserJWT(**authfunc.jwt_decode(jwt))
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


@router.post('/register', response_model=schema.JWT)
async def register(
    user_in: schema.UserCreate,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    register, string should be shown to client
    """
    if crud.user.get_by_email(db, user_in.email):
        return '邮箱已存在'
    user_in.hashed_password = authfunc.encrypt_password(user_in.password)
    user = crud.user.create(db, user_in, is_superuser=False)
    token = jwt.create_access_token(
        schema.UserJWT(
            id = user.id,
            iss = user.name,
            email = user.email,
            is_active = user.is_active,
            is_superuser = user.is_superuser,
            exp = None
        )
    )
    return {"access_token": token}


@router.post('/drop-user')
async def drop_user(
    id: str,
    db: Session = Depends(deps.get_db)
) -> Any:
    if crud.user.get_by_name(db, id):
        return crud.user.drop(db, id)
    return 'no such user'
