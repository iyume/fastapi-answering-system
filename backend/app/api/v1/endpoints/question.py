from typing import Optional, Any

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.api import deps

router = APIRouter(prefix='/question')

@router.get('/')
async def get_question(
    subject: Optional[str] = None,
    db: Session = Depends(deps.get_db)
) -> Any:
    if subject:
        question = crud.item.get_by_random(db, subject=subject)
    else:
        question = crud.item.get_by_random(db)
    if not question:
        raise HTTPException(status_code=400, detail='bad subject')
    return question
