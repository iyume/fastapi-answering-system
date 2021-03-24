from typing import Optional, Any
import asyncio

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import HTMLResponse

from app.config import templates
from app.routers import deps
from app.api import apifunc, userfunc
from app.models import Subjects, UserPayload
from app.security import login_required


router = APIRouter(prefix='/paper')


@router.get('/{subject}/random', response_class=HTMLResponse)
@login_required
async def tiku_paper_random(
    request: Request,
    subject: str,
    subjects: Subjects = Depends(deps.get_subjects),
    current_user: UserPayload = Depends(deps.get_current_user)
) -> Any:
    """
    Render random question-select practice page
    """
    if subject not in subjects.aliases:
        raise HTTPException(status_code=404, detail='Subject not found')
    question = await apifunc.get_question_by_subject(subject, is_random=True)
    return templates.TemplateResponse(
        'paper/practice_random.jinja2', {
            'request': request,
            'current_user': current_user,
            'question': question,
            'subjects': subjects
        }
    )


@router.get('/{subject}/order/{order}', response_class=HTMLResponse)
@login_required
async def tiku_paper_order(
    request: Request,
    subject: str,
    order: int,
    subjects: Subjects = Depends(deps.get_subjects),
    current_user: UserPayload = Depends(deps.get_current_user)
) -> Any:
    """
    order practice page
    """
    if subject not in subjects.aliases:
        raise HTTPException(status_code=404, detail='Subject not found')
    subject_dict = subjects.get_item(subject)
    if not (0 < order <= subject_dict['question_count']):
        raise HTTPException(status_code=404, detail='Order exceeded')
    question_list, question, answer_records = await asyncio.gather(
        apifunc.get_question_by_subject(subject, full=True, is_simple=True),
        apifunc.get_question_by_order(subject, order),
        userfunc.read_answer_caches(current_user.name, unique=True)
    )
    if len(question_list) < subject_dict['question_count']:
        raise HTTPException(status_code=200, detail='内部数据校对错误')
    return templates.TemplateResponse(
        'paper/practice_order.jinja2', {
            "request": request,
            "current_user": current_user,
            "subjects": subjects,
            "question": question,
            "question_list": question_list,
            "answer_records": answer_records
        }
    )
