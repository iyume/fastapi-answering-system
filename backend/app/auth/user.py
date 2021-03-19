from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from app import crud
from app.auth import deps, authfunc
from app import schema


router = APIRouter(prefix='/user')


@router.get('/')
async def list_users(
    db: Session = Depends(deps.get_db)
) -> Any:
    result = crud.user.get_all(db)
    return result


@router.get('')
async def query_user_by_id(
    id: str,
    db: Session = Depends(deps.get_db)
) -> Any:
    user = crud.user.get_by_id(db, id)
    return user


@router.get('/exams')
async def user_all_exams(
    username: str,
    db: Session = Depends(deps.get_db)
) -> Any:
    return crud.examquerycomplex.read_user_all_exams(db, username)


@router.post('/change-password')
async def change_password(
    password_in: schema.UserChangePassword,
    db: Session = Depends(deps.get_db)
) -> Any:
    hashed_password = authfunc.encrypt_password(password_in.password_new)
    crud.user.update_password(db, password_in.id, hashed_password)
    return 'success'


@router.post('/delete')
async def delete_user(
    id: str,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    delete user by id
    """
    crud.user.delete(db, id=id)
    return 'success'
