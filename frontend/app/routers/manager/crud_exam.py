from typing import Any

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from starlette.requests import Request

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
async def list_exam(
    request: Request,
    current_user: schema.UserPayload = Depends(deps.get_current_user)
) -> Any:
    """
    list exams like a dashboard contains `full_info`, `revise`, `delete` button
    """
    ...


@router.get('/{tag}/read')
async def read_exam(
    request: Request,
    tag: str,
    current_user: schema.UserDetail = Depends(deps.get_current_user)
) -> Any:
    ...


@router.get('/{tag}/update')
@superuser_required
async def update_exam(
   request: Request,
   tag: str,
   current_user: schema.UserPayload = Depends(deps.get_current_user) 
) -> Any:
    if not await apifunc.exam_get_by_tag(tag=tag):
        raise HTTPException(status_code=400, detail='无此考试标签')


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
    ...


@router.post('/{tag}/delete')
@superuser_required
async def delete_exam(
    request: Request,
    tag: str,
    current_user: schema.UserPayload = Depends(deps.get_current_user)
) -> Any:
    await apifunc.exam_delete(tag)
    return templates.TemplateResponse(
        'manager/create-exam.jinja2', {
            'request': request,
            'current_user': current_user,
            'message': f"删除考试 {tag} 成功"
        }
    )
