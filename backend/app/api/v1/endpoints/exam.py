from typing import Any

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app import crud, schema
from app.api import deps


router = APIRouter(prefix='/exam')


@router.get('/')
async def list_exam(
    db: Session = Depends(deps.get_db)
) -> Any:
    return crud.examinfo.fetchall(db)


@router.get('')
async def get_exam(
    tag: str,
    db: Session = Depends(deps.get_db)
) -> Any:
    return crud.examinfo.get_by_tag(db, tag=tag)


@router.post('/create')
async def create_exam(
    examinfo: schema.ExamCreate,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    create exam
    """
    return crud.examinfo.create(db, examinfo)


@router.post('/update')
async def update_exam(
    examupdate: schema.ExamUpdate,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    update exam info
    """
    return crud.examinfo.update(db, examupdate)


@router.post('/delete')
async def delete_exam(
    tag: str,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    delete exam by unique tag
    """
    crud.examinfo.delete(db, tag=tag)
    return 'success'


@router.post('/paper/create')
async def create_exam_paper(
    obj_in: schema.ExamBase,
    db: Session = Depends(deps.get_db)
) -> Any:
    exam = crud.examinfo.get_by_tag(db, tag=obj_in.exam_tag)
    if not exam:
        raise HTTPException(status_code=400, detail='Bad exam_tag')
    if not (user := crud.user.get_by_name(db, obj_in.username)) or not user.is_active:
        raise HTTPException(status_code=400, detail='Bad username')
    if crud.examcache.fetchone(db, obj_in):
        return 'exists'
    questions = crud.item.get_by_random_many(
        db,
        amount = exam.question_count,
        subject = exam.subject)
    question_id_list = [question.id for question in questions]
    del questions
    crud.examcache.create_paper(
        db,
        obj_in = obj_in,
        question_id_list = question_id_list
    )
    return 'success'


@router.post('/paper/status')
async def status_exam_paper(
    obj_in: schema.ExamBase,
    db: Session = Depends(deps.get_db)
) -> Any:
    return crud.examcache.paper_status(db, obj_in)


@router.post('/paper/finish')
async def finish_exam_paper(
    obj_in: schema.ExamStatusUpdate,
    db: Session = Depends(deps.get_db)
) -> Any:
    crud.examcache.finish_paper(db, obj_in)


@router.post('/paper/fetchone')
async def exam_paper_fetchone(
    obj_in: schema.ExamBase,
    db: Session = Depends(deps.get_db)
) -> Any:
    return crud.examcache.fetchone(db, obj_in)


@router.post('/paper/')
async def exam_paper_user_all(
    obj_in: schema.ExamPaperQuery,
    db: Session = Depends(deps.get_db)
) -> Any:
    return crud.examcache.get_by_condition(db, obj_in)


@router.post('/paper/first-not-picked')
async def get_first_not_picked_question_exam_paper(
    obj_in: schema.ExamBase,
    db: Session = Depends(deps.get_db)
) -> Any:
    return crud.examcache.get_first_not_picked(db, obj_in)


@router.post('/paper/update-picked')
async def update_exam_paper_picked(
    obj_in: schema.ExamPaperUpdate,
    db: Session = Depends(deps.get_db)
) -> Any:
    return crud.examcache.update_picked(db, obj_in)
