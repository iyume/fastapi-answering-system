from typing import Any
from datetime import datetime

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.config import templates
from app.security import login_required
from app.routers import deps
from app import schema
from app.api import apifunc
from app.models.subject import Subjects


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


@router.get('/complete/{tag}')
@login_required
async def exam_complete(
    request: Request,
    tag: str,
    current_user: schema.UserPayload = Depends(deps.get_current_user)
) -> Any:
    exam: dict = await apifunc.exam_get_by_tag(tag)
    if not exam:
        raise HTTPException(status_code=404)
    exam_paper_status = await apifunc.exam_paper_status(username=current_user.name, exam_tag=tag)
    if exam_paper_status and exam_paper_status.get('status', None):
        exam_records = await apifunc.exam_paper_fetchall(
            username = current_user.name,
            exam_tag = tag
        )
        for i in exam_records:
            if i['picked'] is None:
                return RedirectResponse(
                    request.url_for(
                        'exam_paper_answering',
                        tag = i['exam_tag'],
                        q_num = i['question_order']
                    ),
                    status_code = 303
                )
        await apifunc.exam_paper_finish(current_user.name, tag)
    return RedirectResponse(
        request.url_for('exam_answer', tag = tag, q_num = 1), status_code = 303
    )


@router.get('/tag/{tag}')
async def exam_paper(
    tag: str
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
@router.post('/tag/{tag}/{q_num}')
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
        raise HTTPException(status_code=404)
    exam_status = await apifunc.exam_paper_status(current_user.name, tag)
    if exam_status and exam_status.get('status') == 2:
        return RedirectResponse(
            request.url_for('exam_answer', tag=tag, q_num=1),
            status_code = 303
        )
    if not await apifunc.exam_paper_fetchone(username=current_user.name, exam_tag=tag):
        await apifunc.exam_paper_create(username=current_user.name, exam_tag=tag)
    # update database picked
    if request.method == 'POST':
        form = await request.form()
        await apifunc.exam_paper_update_picked(
            username = current_user.name,
            exam_tag = tag,
            question_id = form['id'],
            picked = form['picked']
        )
        # last question then do nothing
        if q_num == exam['question_count']:
            return RedirectResponse(
                request.url_for('exam_paper_answering', tag=tag, q_num=q_num),
                status_code = 303
            )
        return RedirectResponse(
            request.url_for('exam_paper_answering', tag=tag, q_num=q_num+1),
            status_code = 303
        )
    exam_record = await apifunc.exam_paper_get_by_order(
        username = current_user.name,
        exam_tag = tag,
        question_order = q_num
    )
    exam_records = await apifunc.exam_paper_fetchall(
        username = current_user.name,
        exam_tag = tag
    )
    question = await apifunc.get_answer(id=exam_record['question_id'])
    return templates.TemplateResponse(
        'paper/exam.jinja2', {
            'request': request,
            'current_user': current_user,
            'exam': exam,
            'question': question,
            'exam_records': exam_records,
            'exam_picked': exam_record['picked']
        }
    )


@router.get('/answer/{tag}/{q_num}')
@login_required
async def exam_answer(
    request: Request,
    tag: str,
    q_num: int,
    current_user: schema.UserPayload = Depends(deps.get_current_user)
) -> Any:
    exam: dict = await apifunc.exam_get_by_tag(tag)
    if not exam:
        raise HTTPException(status_code=404)
    if q_num > exam['question_count']:
        raise HTTPException(status_code=404)
    exam_status = await apifunc.exam_paper_status(current_user.name, tag)
    if not (exam_status or exam_status.get('status') != 2):
        return RedirectResponse(
            request.url_for('exam_paper_answering', tag=tag, q_num=q_num)
        )
    exam_record = await apifunc.exam_paper_get_by_order(
        username = current_user.name,
        exam_tag = tag,
        question_order = q_num
    )
    exam_records = await apifunc.exam_paper_fetchall(
        username = current_user.name,
        exam_tag = tag
    )
    question_list = await apifunc.get_answer_many([i['question_id'] for i in exam_records])
    question = question_list[q_num-1]
    return templates.TemplateResponse(
        'exam/answer.jinja2', {
            'request': request,
            'current_user': current_user,
            'question': question,
            'question_list': question_list,
            'exam': exam,
            'exam_records': exam_records,
            'picked': exam_record['picked']
        }
    )
