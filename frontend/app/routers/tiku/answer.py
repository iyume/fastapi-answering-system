from typing import Any

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse

from app.config import templates
from app.routers import deps
from app.api import apifunc
from app.security import login_required
from app import schema
from app.models.subject import Subjects


router = APIRouter(prefix='/answer')


@router.post('/', response_class=HTMLResponse)
@login_required
async def get_answer(
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
