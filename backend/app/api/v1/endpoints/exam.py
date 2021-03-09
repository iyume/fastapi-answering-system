from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schema
from app.api import deps


router = APIRouter(prefix='/exam')


@router.get('/')
async def list_exam(
    db: Session = Depends(deps.get_db)
) -> Any:
    return crud.exam.fetchall(db)


@router.get('')
async def get_exam(
    tag: str,
    db: Session = Depends(deps.get_db)
) -> Any:
    return crud.exam.get_by_tag(db, tag=tag)


@router.post('/create')
async def create_exam(
    examinfo: schema.ExamCreate,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    create exam
    """
    return crud.exam.create(db, examinfo)


@router.post('/delete')
async def delete_exam(
    tag: str,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    delete exam by unique tag
    """
    crud.exam.delete(db, tag=tag)
    return 'success'
