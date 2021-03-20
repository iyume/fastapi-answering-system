from typing import Any
from datetime import datetime

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.config import templates
from app.routers import deps
from app import schema
from app.security import superuser_required
from app.api import apifunc
from app.models import Subjects


router = APIRouter(prefix='/exam')


@router.get('/create')
@superuser_required
async def create_exam(
    request: Request,
    current_user: schema.UserPayload = Depends(deps.get_current_user)
) -> Any:
    return templates.TemplateResponse(
        'manager/create-exam.jinja2', {
            'request': request,
            'current_user': current_user
        }
    )


@router.post('/create')
@superuser_required
async def create_exam_action(
    request: Request,
    subjects: Subjects = Depends(deps.get_subjects),
    current_user: schema.UserPayload = Depends(deps.get_current_user)
) -> Any:
    form = await request.form()
    if await apifunc.exam_get_by_tag(form['tag']):
        return templates.TemplateResponse(
            'manager/create-exam.jinja2', {
                'request': request,
                'current_user': current_user,
                'message': '考试标签重复'
            }
        )
    # start_time = datetime.fromisoformat(form['start_time'])
    # end_time = datetime.fromisoformat(form['end_time'])
    start_time = form['start_time_date'] + 'T' + form['start_time_time']
    end_time = form['end_time_date'] + 'T' + form['end_time_time']
    created_exam = await apifunc.exam_create(
        title = form['title'],
        tag = form['tag'],
        type = form['type'],
        subject = form['subject'],
        question_count = int(form['question_count']),
        start_time = start_time,
        end_time = end_time,
        detail = form['detail']
    )
    return templates.TemplateResponse(
        'manager/create-exam.jinja2', {
            'request': request,
            'current_user': current_user,
            'subjects': subjects,
            'created_exam': created_exam
        }
    )


@router.get('/list')
@superuser_required
async def list_exam(
    request: Request,
    current_user: schema.UserPayload = Depends(deps.get_current_user)
) -> Any:
    """
    list exams like a dashboard contains `full_info`, `revise`, `delete` button
    """
    exams: list = await apifunc.exam_fetchall()
    if exams:
        for exam in exams:
            start_time = datetime.fromisoformat(exam['start_time'])
            end_time = datetime.fromisoformat(exam['end_time'])
            exam['start_time'] = exam['start_time'].replace('T', ' ')
            exam['end_time'] = exam['end_time'].replace('T', ' ')
            if timenow := datetime.now():
                if start_time < timenow < end_time:
                    exam['opening_status'] = '进行中'
                elif timenow > end_time:
                    exam['opening_status'] = '已结束'
                else:
                    exam['opening_status'] = '未开始'
    return templates.TemplateResponse(
        'manager/list-exam.jinja2', {
            'request': request,
            'current_user': current_user,
            'exams': exams,
        }
    )


@router.get('/{tag}/read')
@superuser_required
async def read_exam(
    request: Request,
    tag: str,
    subjects: Subjects = Depends(deps.get_subjects),
    current_user: schema.UserDetail = Depends(deps.get_current_user)
) -> Any:
    if not await apifunc.exam_get_by_tag(tag=tag):
        raise HTTPException(status_code=400, detail='无此考试标签')
    exam = await apifunc.exam_get_by_tag(tag)
    return templates.TemplateResponse(
        'manager/create-exam.jinja2', {
            'request': request,
            'current_user': current_user,
            'subjects': subjects,
            'created_exam': exam,
            'is_read_exam': True,
        }
    )


@router.get('/{tag}/update')
@superuser_required
async def update_exam(
   request: Request,
   tag: str,
   subjects: Subjects = Depends(deps.get_subjects),
   current_user: schema.UserPayload = Depends(deps.get_current_user) 
) -> Any:
    if not await apifunc.exam_get_by_tag(tag=tag):
        raise HTTPException(status_code=400, detail='无此考试标签')
    to_update = await apifunc.exam_get_by_tag(tag)
    to_update['start_time_date'], to_update['start_time_time'] = to_update['start_time'].split('T', 1)
    to_update['end_time_date'], to_update['end_time_time'] = to_update['end_time'].split('T', 1)
    return templates.TemplateResponse(
        'manager/create-exam.jinja2', {
            'request': request,
            'current_user': current_user,
            'subjects': subjects,
            'to_update': to_update
        }
    )


@router.post('/{tag}/update')
@superuser_required
async def update_exam_action(
   request: Request,
   tag: str,
   current_user: schema.UserPayload = Depends(deps.get_current_user) 
) -> Any:
    """
    update do not revise tag
    """
    if not await apifunc.exam_get_by_tag(tag=tag):
        raise HTTPException(status_code=400, detail='无此考试标签')
    form = await request.form()
    start_time = form['start_time_date'] + 'T' + form['start_time_time']
    end_time = form['end_time_date'] + 'T' + form['end_time_time']
    await apifunc.exam_update(
        title = form['title'],
        tag = tag,
        type = form['type'],
        subject = form['subject'],
        question_count = int(form['question_count']),
        start_time = start_time,
        end_time = end_time,
        detail = form['detail']
    )
    return RedirectResponse(request.url_for('list_exam'), status_code=303)


@router.get('/{tag}/delete')
@superuser_required
async def delete_exam(
    request: Request,
    tag: str,
    current_user: schema.UserPayload = Depends(deps.get_current_user)
) -> Any:
    return templates.TemplateResponse(
        'manager/check.jinja2', {
            'request': request,
            'current_user': current_user,
            'check_delete_exam': True
        }
    )


@router.post('/{tag}/delete')
@superuser_required
async def delete_exam_action(
    request: Request,
    tag: str,
    current_user: schema.UserPayload = Depends(deps.get_current_user)
) -> Any:
    await apifunc.exam_delete(tag)
    exams = await apifunc.exam_fetchall()
    if exams:
        for exam in exams:
            start_time = datetime.fromisoformat(exam['start_time'])
            end_time = datetime.fromisoformat(exam['end_time'])
            exam['start_time'] = exam['start_time'].replace('T', ' ')
            exam['end_time'] = exam['end_time'].replace('T', ' ')
            if timenow := datetime.now():
                if start_time < timenow < end_time:
                    exam['opening_status'] = '进行中'
                elif timenow > end_time:
                    exam['opening_status'] = '已结束'
                else:
                    exam['opening_status'] = '未开始'
    return templates.TemplateResponse(
        'manager/list-exam.jinja2', {
            'request': request,
            'current_user': current_user,
            'exams': exams,
            'message': f"删除考试 {tag} 成功"
        }
    )
