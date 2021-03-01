from fastapi import APIRouter
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session

from app import crud
from app.auth import deps
from app.models.user import User


router = APIRouter()

@router.post('/user')
async def list_users(
    db: Session = Depends(deps.get_db)
):
    return crud.user.get_all(db)

@router.post('/user/{name}')
async def inspect_user(name: str):
    result = User(name)
    return result
