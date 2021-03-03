from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import HTMLResponse

from app.config import templates
from app.routers.tiku import deps
from app.models import Subjects, User


router = APIRouter(prefix='/area')


@router.get('', response_class=HTMLResponse)
@router.get('/', response_class=HTMLResponse)
async def tiku_area_index(
    request: Request,
    subjects: Subjects = Depends(deps.get_subjects),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Render index page, but not the final index page
    """
    return templates.TemplateResponse(
        'tiku/area/base.jinja2',
        {
            'request': request,
            'subjects': subjects
        }
    )

@router.get('/{subject}', response_class=HTMLResponse)
async def tiku_area(
    request: Request,
    subject: str,
    subjects: Subjects = Depends(deps.get_subjects),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Enter the selected subject navigation page
    """
    if subject not in subjects.aliases:
        raise HTTPException(status_code=404, detail='Subject not found')
    request._query_params = {}
    request._query_params['type'] = 'random'
    return templates.TemplateResponse(
        'tiku/area/subject.jinja2',
        {
            'request': request,
            'subjects': subjects
        }
    )
