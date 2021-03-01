from fastapi import APIRouter, Depends

from sqlalchemy.orm.session import Session

from app import schema, crud
from app.auth import deps, func

router = APIRouter(prefix='/auth', tags=['auth'])

@router.post('/access-token')
async def access_token(
    name: str,
    password: str
):
    return func.validate(name, password)

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
    if crud.user.get_by_email(db, user_in.email) or crud.user.get_by_name(db, user_in.name):
        return 'Existed email or name'
    user = crud.user.create(db, user_in, is_superuser=False)
    return user
