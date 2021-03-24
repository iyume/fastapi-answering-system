from typing import Optional, Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud
from app.api import deps


router = APIRouter(prefix='/question')


@router.get('/')
async def get_question(
    qid: Optional[str] = None,
    subject: Optional[str] = None,
    is_simple: bool = True,
    db: Session = Depends(deps.get_db)
) -> Any:
    if qid:
        return crud.item.get_by_id(db, qid)
    if subject:
        results = crud.item.get_by_subject_all(db, subject)
        if not is_simple:
            return results
        return [
            {
                "question_id": result.id,
                "answer": result.answer
            }
            for result in results
        ]
    return 'no function'


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
    return crud.item.get_by_subject_order(db, subject, order)
