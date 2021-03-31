from typing import Any
import asyncio

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse

from app.config import templates
from app.routers import deps
from app.api import apifunc, userfunc
from app.security import login_required
from app import schema
from app.models.subject import Subjects


router = APIRouter(prefix='/answer')


@router.post('/random', response_class=HTMLResponse)
@login_required
async def get_answer_random(
    request: Request,
    subjects: Subjects = Depends(deps.get_subjects),
    current_user: schema.UserPayload = Depends(deps.get_current_user)
) -> Any:
    """
    Render answer page according to the answer selected in paper
    """
    form = await request.form()
    if 'qid' not in form or 'picked' not in form:
        return RedirectResponse(request.url_for('index'))
    qid = form['qid']
    picked = form['picked']
    subject = form['subject']
    if picked not in list('ABCD'):
        raise HTTPException(status_code=400, detail='Bad picked')
    question = await apifunc.get_answer(qid)
    await userfunc.create_answer_cache(
        username = current_user.name,
        question_id = question['id'],
        picked = picked,
        paper_type = 'random',
        subject = subject
    )
    return templates.TemplateResponse(
        'answer/practice_random.jinja2', {
            'request': request,
            'subjects': subjects,
            'current_user': current_user,
            'question': question,
            'picked': picked,
            'subject': subject
        }
    )


@router.post('/order', response_class=HTMLResponse)
@login_required
async def get_answer_order(
    request: Request,
    subjects: Subjects = Depends(deps.get_subjects),
    current_user: schema.UserPayload = Depends(deps.get_current_user)
) -> Any:
    """
    Render answer page according to the answer selected in paper
    """
    form = await request.form()
    qid = form['qid']
    picked = form['picked']
    subject = form['subject']
    order = form['order']
    if picked not in list('ABCD'):
        raise HTTPException(status_code=400, detail='Bad picked')
    await userfunc.create_answer_cache(
        username = current_user.name,
        question_id = qid,
        picked = picked,
        paper_type = 'order',
        subject = subject
    )
    question_list, question, answer_records = await asyncio.gather(
        apifunc.get_question_by_subject(subject, full=True, is_simple=True),
        apifunc.get_answer(qid),
        userfunc.read_answer_caches(current_user.name, unique=True)
    )
    done_qid_set = set({d['question_id'] for d in answer_records})
    for d in question_list:
        if d['question_id'] in done_qid_set:
            d.update(
                {
                    'picked': i['picked']
                    for i in answer_records
                    if i['question_id'] == d['question_id']
                }
            )
    return templates.TemplateResponse(
        'answer/practice_order.jinja2', {
            'request': request,
            'subjects': subjects,
            'current_user': current_user,
            'question': question,
            'picked': picked,
            'subject': subjects.get_item(subject),
            'question_order': int(order),
            'question_list': question_list,
            'answer_records': answer_records
        }
    )
