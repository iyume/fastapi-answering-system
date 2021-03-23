from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from app import crud
from app.api.auth import deps
from app import schema


router = APIRouter(prefix='/answer-cache')


@router.get('/')
async def user_answer_cache(
    username: str,
    db: Session = Depends(deps.get_db)
) -> Any:
    return crud.itemcache.query_userall_unique(db, username)


@router.post('/')
async def user_answer_cache_create(
    obj_in: schema.ItemCacheCreate,
    db: Session = Depends(deps.get_db)
) -> Any:
    return crud.itemcache.create(db, obj_in)


@router.post('/refresh')
async def user_answer_cache_refresh(
    username: str,
    db: Session = Depends(deps.get_db)
) -> Any:
    return crud.itemcache.refresh(db, username)
