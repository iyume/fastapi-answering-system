from typing import Any
import asyncio

from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException
from starlette.requests import Request

from app.config import templates
from app.routers import deps
from app.security import superuser_required
from app.models import UserPayload
from app.api import userfunc, apifunc
from app.func import read_exams
from app.models import Subjects


router = APIRouter(prefix='/user-activity')


@router.get('/')
@superuser_required
async def manage_list_userinfo(
    request: Request,
    current_user: UserPayload = Depends(deps.get_current_user)
) -> Any:
    users = await userfunc.get_all_user()
    return templates.TemplateResponse(
        'manager/user-statusboard.jinja2', {
            'request': request,
            'current_user': current_user,
            'users': users
        }
    )


@router.get('/{username}/exams')
@superuser_required
async def manage_list_user_exams(
    request: Request,
    username: str,
    subjects: Subjects = Depends(deps.get_subjects),
    current_user: UserPayload = Depends(deps.get_current_user)
) -> Any:
    if not await userfunc.get_by_name(username):
        raise HTTPException(status_code=400, detail='Bad username')
    userexams = await read_exams(username)
    return templates.TemplateResponse(
        'user/myexams.jinja2', {
            "request": request,
            "current_user": current_user,
            "subjects": subjects,
            "myexams": userexams
        }
    )


@router.get('/{username}/exam/{exam_tag}/{q_num}')
@superuser_required
async def manage_inspect_user_exam(
    request: Request,
    username: str,
    exam_tag: str,
    q_num: int,
    current_user: UserPayload = Depends(deps.get_current_user)
) -> Any:
    user, exam, exam_status = await asyncio.gather(
        userfunc.get_by_name(username),
        apifunc.exam_get_by_tag(exam_tag),
        apifunc.exam_paper_status(username, exam_tag)
    )
    if not user:
        raise HTTPException(status_code=400, detail='Bad username')
    if not exam:
        raise HTTPException(status_code=400, detail='Bad exam tag')
    if not (0 < q_num <= exam['question_count']):
        raise HTTPException(status_code=404)
    if not (exam_status or exam_status.get('status') != 2):
        raise HTTPException(status_code=200, detail='考试未完成，无法查看')
    exam_records = await apifunc.exam_paper_fetchall(
        username = username,
        exam_tag = exam_tag
    )
    exam_record = exam_records[q_num-1]
    question_list = await apifunc.get_answer_many([i['question_id'] for i in exam_records])
    question = await apifunc.get_answer(question_list[q_num-1]['question_id'])
    return templates.TemplateResponse(
        'answer/exam.jinja2', {
            'request': request,
            'current_user': current_user,
            'question': question,
            'question_list': question_list,
            'exam': exam,
            'exam_records': exam_records,
            'picked': exam_record['picked']
        }
    )
