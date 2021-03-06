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


@router.get('/{subject}', response_class=HTMLResponse)
@login_required
async def tiku_paper(
    request: Request,
    subject: str,
    type: str = None,
    id: Optional[str] = None,
    picked: Optional[str] = None,
    subjects: Subjects = Depends(deps.get_subjects),
    current_user: UserPayload = Depends(deps.get_current_user)
) -> Any:
    """
    Case1:
        Render random question-select practice page
    Case2:
        Render answer page according to selected option
    if (id & picked) -> Case2
    """
    ## Case 2
    if id and picked:
        question = await apifunc.get_answer(id)
        return templates.TemplateResponse(
            'tiku/paper/subject.jinja2', {
                'request': request,
                'question': question,
                'subjects': subjects,
                'picked': picked
            }
        )

    ## Case 1
    if subject not in subjects.aliases:
        raise HTTPException(status_code=404, detail='Subject not found')
    if not type:
        raise HTTPException(status_code=422, detail='Missing type parameter')
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
