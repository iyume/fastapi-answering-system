from typing import Any

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from starlette.requests import Request

from app.config import templates
from app.routers import deps
from app.models import UserPayload
from app.security import superuser_required


router = APIRouter(prefix='/user')


@router.get('/')
@superuser_required
async def list_user(
    request: Request,
    current_user: UserPayload = Depends(deps.get_current_user)
) -> Any:
    raise HTTPException(status_code=200, detail='考生账户管理功能暂未开放')


@router.post('/update')
@superuser_required
async def update_user(
    request: Request,
    current_user: UserPayload = Depends(deps.get_current_user)
) -> Any:
    ...


@router.post('/delete')
@superuser_required
async def delete_user(
    request: Request,
    current_user: UserPayload = Depends(deps.get_current_user)
) -> Any:
    ...
