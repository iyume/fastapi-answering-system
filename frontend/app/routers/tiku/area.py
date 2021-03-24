from typing import Any

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import HTMLResponse

from app.config import templates
from app.routers import deps
from app.models import Subjects, UserPayload
from app.api import userfunc
from app.security import login_required


router = APIRouter(prefix='/area')


@router.get('/', response_class=HTMLResponse)
@router.post('/', response_class=HTMLResponse)
async def tiku_area_index(
    request: Request,
    subjects: Subjects = Depends(deps.get_subjects),
    current_user: UserPayload = Depends(deps.get_current_user)
) -> Any:
    """
    Render index page, but not the final index page
    """
    return templates.TemplateResponse(
        'area/base.jinja2',
        {
            'request': request,
            'current_user': current_user,
            'subjects': subjects
        }
    )


@router.get('/{subject}', response_class=HTMLResponse)
@router.post('/{subject}', response_class=HTMLResponse)
@login_required
async def tiku_area(
    request: Request,
    subject: str,
    subjects: Subjects = Depends(deps.get_subjects),
    current_user: UserPayload = Depends(deps.get_current_user)
) -> Any:
    """
    Enter the selected subject navigation page
    """
    if subject not in subjects.aliases:
        raise HTTPException(status_code=404, detail='Subject not found')
    done_count: dict = await userfunc.read_answered_count(current_user.name)
    return templates.TemplateResponse(
        'area/subject.jinja2',
        {
            'request': request,
            'current_user': current_user,
            'subjects': subjects,
            'done_count': done_count
        }
    )
