from typing import Optional, Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud
from app.api import deps


router = APIRouter(prefix='/question')


@router.get('/')
async def get_question(
    qid: str,
    db: Session = Depends(deps.get_db)
) -> Any:
    return crud.item.get_by_id(db, qid)


@router.get('/random')
async def get_question_random(
    subject: Optional[str] = None,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    get question
    """
    if subject:
        return crud.item.get_by_random(db, subject)
    else:
        return crud.item.get_by_random(db)


@router.get('/order')
async def get_question_order(
    subject: str,
    order: int,
    db: Session = Depends(deps.get_db)
) -> Any:
    return crud.item.get_by_order(db, subject, order)
