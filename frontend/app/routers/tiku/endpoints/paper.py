from typing import List
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import HTMLResponse

from app.config import templates
from app.routers.tiku import deps
from app.api import apifunc
from app.models.subject import Subjects
from app.models.user import User
from app.login import login_required

router = APIRouter(prefix='/paper')


@router.get('/{subject}', response_class=HTMLResponse)
@login_required
async def tiku_paper(
    request: Request,
    subject: str,
    type: str = None,
    subjects: Subjects = Depends(deps.get_subjects),
    current_user: User = Depends(deps.get_current_user)
):
    if not type:
        raise HTTPException(status_code=422, detail='Missing type parameter')
    if subject not in subjects.aliases:
        raise HTTPException(status_code=404, detail='Subject not found')
    request._query_params = {}
    request._query_params['type'] = type
    if type == 'random':
        question = await apifunc.get_question_by_subject(subject)
        return templates.TemplateResponse(
            'tiku/paper/subject.jinja2', {
                'request': request,
                'question': question,
                'subjects': subjects
            }
        )
    else:
        raise HTTPException(status_code=400, detail='Bad request')
