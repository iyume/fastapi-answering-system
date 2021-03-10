from typing import Any
from datetime import datetime

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from starlette.requests import Request

from app.config import templates
from app.security import login_required
from app.routers import deps
from app import schema
from app.api import apifunc


router = APIRouter()


@router.get('/entry')
@login_required
async def exam_entry(
    request: Request,
    current_user: schema.UserPayload = Depends(deps.get_current_user)
) -> Any:
    exams = await apifunc.exam_fetchall()
    unstarted_exams: list[dict] = []
    processing_exams: list[dict] = []
    finished_exams: list[dict] = []
    for exam in exams:
        exam['start_time'] = datetime.fromisoformat(exam['start_time'])
        exam['end_time'] = datetime.fromisoformat(exam['end_time'])
        if exam['start_time'] > datetime.now():
            unstarted_exams.append(exam)
        if exam['end_time'] < datetime.now():
            finished_exams.append(exam)
        if exam['start_time'] < datetime.now() < exam['end_time']:
            processing_exams.append(exam)
    for exam in exams:
        exam['start_time'] = datetime.strftime(exam['start_time'], '%F %X')
        exam['end_time'] = datetime.strftime(exam['end_time'], '%F %X')
    return templates.TemplateResponse(
        'exam/entry.jinja2', {
            'request': request,
            'current_user': current_user,
            'unstarted_exams': unstarted_exams,
            'processing_exams': processing_exams,
            'finished_exams': finished_exams
        }
    )


@router.post('/submit')
@login_required
async def exam_submit(
    request: Request,
    current_user: schema.UserPayload = Depends(deps.get_current_user)
) -> Any:
    form = await request.form()
    try:
        exam_tag = form['exam_tag']
        question_order = int(form['question_order'])
    except:
        raise HTTPException(status_code=403)
    if not (exam := await apifunc.exam_paper_get_by_order(
        user_id = current_user.id,
        exam_tag = exam_tag,
        question_order = question_order
    )):
        raise HTTPException(status_code=400, detail='Bad exam_tag or question_order')
    # do database update


@router.get('/complete')
@login_required
async def exam_complete(
    request: Request,
    exam_tag: str,
    current_user: schema.UserPayload = Depends(deps.get_current_user)
) -> Any:
    if not (exam := await apifunc.exam_get_by_tag(exam_tag)):
        raise HTTPException(status_code=400, detail='Bad exam_tag')
    exam_records = await apifunc.exam_paper_fetchall(
        user_id = current_user.id,
        exam_tag = exam_tag
    )
    for i in exam_records:
        if i['picked'] is None:
            raise HTTPException(status_code=200, detail=f"您尚未完成考试 {exam['title']}")
    return exam_records


@router.get('/tag/{tag}')
@login_required
async def exam_paper(
    request: Request,
    tag: str,
    current_user: schema.UserPayload = Depends(deps.get_current_user)
) -> Any:
    exam: dict = await apifunc.exam_get_by_tag(tag)
    if not exam:
        raise HTTPException(status_code=404)
    start_time = datetime.fromisoformat(exam['start_time'])
    end_time = datetime.fromisoformat(exam['end_time'])
    if not (start_time < datetime.now() < end_time):
        raise HTTPException(status_code=403, detail='考试尚未开始或已经结束')
    raise HTTPException(status_code=200, detail='考试进行中，请从主页入口进入')


@router.get('/tag/{tag}/{q_num}')
@login_required
async def exam_paper_answering(
    request: Request,
    tag: str,
    q_num: int,
    current_user: schema.UserPayload = Depends(deps.get_current_user)
) -> Any:
    """
    select question from database according to the question_order column
    """
    exam: dict = await apifunc.exam_get_by_tag(tag)
    if not exam:
        raise HTTPException(status_code=404)
    start_time = datetime.fromisoformat(exam['start_time'])
    end_time = datetime.fromisoformat(exam['end_time'])
    if not (start_time < datetime.now() < end_time):
        raise HTTPException(status_code=403, detail='考试尚未开始或已经结束')
    if q_num > exam['question_count']:
        if q_num == exam['question_count'] + 1:
            raise HTTPException(status_code=200, detail='答题完毕')
        raise HTTPException(status_code=404)
    if not await apifunc.exam_paper_fetchone(user_id=current_user.id, exam_tag=tag):
        await apifunc.exam_paper_create(user_id=current_user.id, exam_tag=tag)
    exam_record = await apifunc.exam_paper_get_by_order(
        user_id = current_user.id,
        exam_tag = tag,
        question_order = 1
    )
    exam_records = await apifunc.exam_paper_fetchall(
        user_id = current_user.id,
        exam_tag = tag
    )
    return f"{exam_record}{exam_records}"
