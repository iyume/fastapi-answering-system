from typing import Any

from fastapi import APIRouter, Depends
from starlette.requests import Request

from app.config import templates
from app.routers import deps
from app import schema
from app.security.func import superuser_required
from app.api import apifunc


router = APIRouter(prefix='/exam')


@router.get('/create')
@superuser_required
async def create_exam(
    request: Request,
    current_user: schema.UserPayload = Depends(deps.get_current_user)
) -> Any:
    return templates.TemplateResponse(
        'user/super/create-exam.jinja2', {
            'request': request,
            'current_user': current_user
        }
    )


@router.post('/create')
@superuser_required
async def create_exam_action(
    request: Request,
    current_user: schema.UserPayload = Depends(deps.get_current_user)
) -> Any:
    form = await request.form()
    if await apifunc.exam_get_by_tag(form['tag']):
        return templates.TemplateResponse(
            'user/super/create-exam.jinja2', {
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
        start_time = start_time,
        end_time = end_time,
        detail = form['detail']
    )
    return templates.TemplateResponse(
        'user/super/create-exam.jinja2', {
            'request': request,
            'current_user': current_user,
            'created_exam': created_exam
        }
    )


@router.post('/delete')
@superuser_required
async def delete_exam(
    request: Request,
    current_user: schema.UserPayload = Depends(deps.get_current_user)
) -> Any:
    form = await request.form()
    await apifunc.exam_delete(form['tag'])
    return templates.TemplateResponse(
        'user/super/create-exam.jinja2', {
            'request': request,
            'current_user': current_user,
            'message': f"删除考试 {form['tag']} 成功"
        }
    )
