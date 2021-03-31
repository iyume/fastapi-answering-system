from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api import deps
from app import crud


router = APIRouter(prefix='/extra', tags=['extrapi'])


@router.post('/clear-answer-cache')
async def user_clear_answer_cache(
    username: str,
    db: Session = Depends(deps.get_db)
) -> Any:
    crud.itemcache.clear(db, username)
    crud.user.update_done_counter(
        db,
        username,
        fb_done_count=0,
        fr_done_count=0,
        sr_done_count=0
    )


@router.post('/refresh-info')
async def refresh_user_info(
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    normalize / modify / correct data
    """
    # correct recent done exam
    exam_statuses = crud.examstatus.query_all(db)
    username_set = set()
    for i in exam_statuses:
        if i.status == 2:
            if i.username not in username_set:
                username_set.add(i.username)
            crud.user.update_recent_done_exam(db, i.username, i.exam_tag)
    return
