from typing import Optional, Any

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import HTMLResponse

from app.config import templates
from app.routers import deps
from app.api import apifunc
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
    question = await apifunc.get_question_by_subject(subject)
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
