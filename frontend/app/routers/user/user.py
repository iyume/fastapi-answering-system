import asyncio
from typing import Any
from datetime import datetime

from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.config import templates
from app.routers import deps
from app import schema
from app.security.func import login_required
from app.api import userfunc, apifunc
from app.models.subject import Subjects


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
    subjects: Subjects = Depends(deps.get_subjects),
    current_user: schema.UserPayload = Depends(deps.get_current_user)
) -> Any:
    if not current_user.name == username:
        return RedirectResponse(request.url_for('homepage'))
    myexams = await userfunc.read_exams(username)
    myexams = sorted(myexams, key=lambda k:k['start_time'], reverse=True)
    processing_exam_entry_coroutines = []
    processing_exam_entry_index = []
    for exam in myexams:
        if exam['exam_status'] == 1:
            processing_exam_entry_coroutines.append(
                apifunc.exam_paper_get_first_not_picked(
                    current_user.name,
                    exam['exam_tag']
                )
            )
            processing_exam_entry_index.append(myexams.index(exam))
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
    processing_exam_entry_coroutines_results = await asyncio.gather(
        *processing_exam_entry_coroutines
    )
    for i, e in zip(
        processing_exam_entry_index,
        processing_exam_entry_coroutines_results
    ):
        # TODO strict zip in python3.10
        myexams[i]['exam_entry_num'] = e.get('question_order', 1) if e else 1
    return templates.TemplateResponse(
        'user/myexams.jinja2', {
            'request': request,
            'subjects': subjects,
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
        await userfunc.change_password(current_user.uid, form.get('password_new'))
        rr = RedirectResponse(request.url_for('login'))
        rr.set_cookie('jwt', value='deleted', expires=0)
        return rr
    return RedirectResponse(request.url_for('homepage'))
