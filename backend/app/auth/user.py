from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from app import crud
from app.auth import deps, authfunc
from app import schema


router = APIRouter(prefix='/user')


@router.post('/')
async def list_users(
    db: Session = Depends(deps.get_db)
) -> Any:
    result = crud.user.get_all(db)
    return result


@router.post('')
async def query_user_by_id(
    id: str,
    db: Session = Depends(deps.get_db)
) -> Any:
    user = crud.user.get_by_id(db, id)
    return user


@router.post('/change-password')
async def change_password(
    password_in: schema.UserChangePassword,
    db: Session = Depends(deps.get_db)
) -> Any:
    hashed_password = authfunc.encrypt_password(password_in.password_new)
    crud.user.update_password(db, password_in.id, hashed_password)
    return 'success'