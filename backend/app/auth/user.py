from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from app import crud
from app.auth import deps


router = APIRouter(prefix='/user')


@router.post('/')
async def list_users(
    db: Session = Depends(deps.get_db)
) -> Any:
    result = crud.user.get_all(db)
    return result

@router.post('/user/{id}')
async def user_id(
    id: str,
    db: Session = Depends(deps.get_db)
) -> Any:
    user = crud.user.get_by_id(db, id)
    return user
