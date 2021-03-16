from datetime import datetime
from typing import Any

from fastapi import APIRouter
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session

from app import crud, schema
from app.auth import deps, authfunc


router = APIRouter(tags=['extrapi'])


@router.post('/test-token')
async def test_token(token: str) -> Any:
    payload = authfunc.jwt_decode(token)
    payload.update(
        {
            'exp_date': datetime.fromtimestamp(payload.get('exp') or 1000000000)
        }
    )
    return payload


@router.post('/create-superuser')
async def register(
    user_in: schema.UserCreate,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    register, string should be shown to client
    """
    if user_in.email and crud.user.get_by_email(db, user_in.email):
        return '邮箱已存在'
    user_in.hashed_password = authfunc.encrypt_password(user_in.password)
    user = crud.user.create(db, user_in, is_superuser=True)
    return user
