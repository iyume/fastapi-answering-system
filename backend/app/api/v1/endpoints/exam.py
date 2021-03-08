from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schema
from app.api import deps


router = APIRouter(prefix='/exam')


@router.post('/create')
async def get_question(
    examinfo: schema.ExamCreate,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    create exam
    """
    return crud.exam.create(db, examinfo)
