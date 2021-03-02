from datetime import datetime

from fastapi import APIRouter
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session

from app import crud
from app.auth import deps, func


router = APIRouter(tags=['test resource'])

@router.post('/user')
async def list_users(db: Session = Depends(deps.get_db)):
    result = crud.user.get_all(db)
    return result

@router.post('/user/{name}')
async def inspect_user(name: str, db: Session = Depends(deps.get_db)):
    result = crud.user.get_by_name(db, name)
    return result

@router.post('/test-token')
async def test_token(token: str):
    payload = func.jwt_decode(token)
    payload.update(
        {
            'exp_date': datetime.fromtimestamp(payload.get('exp') or 1000000000)
        }
    )
    return payload
