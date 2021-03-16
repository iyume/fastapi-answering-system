from typing import Any

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app import crud, schema
from app.api import deps


router = APIRouter(prefix='/extra', tags=['extrapi'])


@router.get('/exam-status/')
async def fetch_all_exam_status(
    db: Session = Depends(deps.get_db)
) -> Any:
    return crud.examstatus.query_all(db)


@router.delete('/exam-status/delete')
async def delete_exam_status(
    fade_key: int,
    db: Session = Depends(deps.get_db)
) -> Any:
    crud.examstatus.delete_by_fadekey(db, fade_key=fade_key)
    return 'success'
