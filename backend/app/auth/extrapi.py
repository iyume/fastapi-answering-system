from datetime import datetime
from typing import Any

from fastapi import APIRouter
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session

from app import crud
from app.auth import deps, authfunc


router = APIRouter(tags=['test resource'])

@router.post('/test-token')
async def test_token(token: str) -> Any:
    payload = authfunc.jwt_decode(token)
    payload.update(
        {
            'exp_date': datetime.fromtimestamp(payload.get('exp') or 1000000000)
        }
    )
    return payload
