from fastapi import APIRouter, Depends

from sqlalchemy.orm.session import Session

from app import schema, crud
from app.models.user import User
from app.auth import deps

router = APIRouter(prefix='/auth', tags=['auth'])

@router.post('/access-token')
async def access_token():
    ...

@router.post('/refresh-token')
async def refresh_token():
    ...

@router.post('/revoke-access')
async def revoke_access():
    ...

@router.post('/revoke-refresh')
async def revoke_refresh():
    ...

@router.post('/register')
async def register(
    user_in: schema.UserCreate,
    db: Session = Depends(deps.get_db)
):
    user = crud.user.create(db, user_in)
    return user


@router.get('/{name}')
async def test(name: str):
    result = User(name)
    return result
