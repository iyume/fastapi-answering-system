from typing import Any
from datetime import datetime

from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.config import templates
from app.routers import deps
from app import schema
from app.security.func import login_required
from app.api import userfunc


router = APIRouter()


@router.get('/{username}')
@login_required
async def homepage(
    request: Request,
    username: str,
    current_user: schema.UserDetail = Depends(deps.get_current_user_detail)
) -> Any:
    if current_user.name == username:
        return templates.TemplateResponse(
            'user/homepage.jinja2', {
                'request': request,
                'current_user': current_user
            }
        )
    return RedirectResponse(request.url_for('index'))


@router.get('/{username}/exams')
@login_required
async def my_exams(
    request: Request,
    username: str,
    current_user: schema.UserPayload = Depends(deps.get_current_user)
) -> Any:
    if not current_user.name == username:
        return RedirectResponse(request.url_for('homepage'))
    myexams = await userfunc.read_exams(current_user.id)
    for exam in myexams:
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
        'user/myexams.jinja2', {
            'request': request,
            'current_user': current_user,
            'myexams': myexams
        }
    )


@router.get('/{username}/change-password')
@login_required
async def change_password(
    request: Request,
    username: str,
    current_user: schema.UserPayload = Depends(deps.get_current_user)
) -> Any:
    if current_user.name == username:
        return templates.TemplateResponse(
            'user/change-password.jinja2', {
                'request': request,
                'current_user': current_user
            }
        )
    return RedirectResponse(request.url_for('homepage'))


@router.post('/{username}/change-password')
@login_required
async def change_password_action(
    request: Request,
    username: str,
    current_user: schema.UserPayload = Depends(deps.get_current_user)
) -> Any:
    if current_user.name == username:
        form = await request.form()
        if form.get('password_new') != form.get('password_new_check'):
            return templates.TemplateResponse(
                'user/change-password.jinja2', {
                    'request': request,
                    'current_user': current_user,
                    'message': '两个密码不同，请重新输入'
                }
            )
        await userfunc.change_password(current_user.id, form.get('password_new'))
        rr = RedirectResponse(request.url_for('login'))
        rr.set_cookie('jwt', value='deleted', expires=0)
        return rr
    return RedirectResponse(request.url_for('homepage'))
