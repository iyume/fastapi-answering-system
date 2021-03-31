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
    unique: bool,
    db: Session = Depends(deps.get_db)
) -> Any:
    if unique:
        return crud.itemcache.query_userall_unique(db, username)
    else:
        return crud.itemcache.query_userall(db, username)


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


@router.get('/count')
async def user_answered_count(
    username: str,
    db: Session = Depends(deps.get_db)
) -> Any:
    user = crud.user.get_by_name(db, username)
    if not user:
        return f'no user named {username}'
    return {
        "fb_done_count": user.fb_done_count,
        "fr_done_count": user.fr_done_count,
        "sr_done_count": user.sr_done_count
    }
