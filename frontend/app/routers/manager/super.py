from typing import Any

from fastapi import APIRouter, Depends
from starlette.requests import Request

from app.config import templates
from app.routers import deps
from app import schema
from app.security.func import superuser_required
from app.api import apifunc


router = APIRouter()


@router.get('/create-exam')
@superuser_required
async def create_exam(
    request: Request,
    current_user: schema.UserPayload = Depends(deps.get_current_user)
) -> Any:
    return templates.TemplateResponse(
        'user/create-exam.jinja2', {
            'request': request,
            'current_user': current_user
        }
    )


@router.post('/create-exam')
@superuser_required
async def create_exam_action(
    request: Request,
    current_user: schema.UserPayload = Depends(deps.get_current_user)
) -> Any:
    form = await request.form()
    # start_time = datetime.fromisoformat(form['start_time'])
    # end_time = datetime.fromisoformat(form['end_time'])
    result = await apifunc.create_exam(
        title = form['title'],
        tag = form['tag'],
        type = form['type'],
        start_time = form['start_time'],
        end_time = form['end_time'],
        detail = form['detail']
    )
    return result
