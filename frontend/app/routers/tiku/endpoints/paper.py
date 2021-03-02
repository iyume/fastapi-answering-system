from typing import List
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import HTMLResponse

from app.config import templates
from app.routers.tiku import deps
from app.api import apifunc
from app.models.subject import Subjects

router = APIRouter(prefix='/paper')


@router.get('/{subject}', response_class=HTMLResponse)
async def tiku_paper_subject(
    request: Request,
    subject: str,
    type: str,
    subjects: Subjects = Depends(deps.get_subjects)
):
    if subject not in subjects:
        raise HTTPException(status_code=404, detail='Subject not found')
    if type == 'random':
        question = await apifunc.get_question_by_subject(subject)
        return templates.TemplateResponse(
            'tiku/paper/fb.jinja2', {
                'request': request,
                'question': question
            }
        )
    else:
        return HTTPException(status_code=400, detail='Bad request')
