from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud
from app.api import deps

router = APIRouter(prefix='/question')

@router.get('/')
async def get_question(
    db: Session = Depends(deps.get_db),
    subject: Optional[str] = None
):
    if subject:
        question = crud.item.get_by_random(db, subject=subject)
    else:
        question = crud.item.get_by_random(db)
    return question
