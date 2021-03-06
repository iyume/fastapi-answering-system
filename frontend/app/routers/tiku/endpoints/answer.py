from typing import Any

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import HTMLResponse

from app.config import templates
from app.routers import deps
from app.api import apifunc
from app.security import login_required
from app import schema


router = APIRouter(prefix='/answer')


@router.get('/', response_class=HTMLResponse)
@login_required
async def tiku_answer(
    request: Request,
    id: str,
    picked: str,
    current_user: schema.UserPayload = Depends(deps.get_current_user)
) -> Any:
    """
    Render answer page according to the answer selected in paper
    """
    if picked not in list('ABCD'):
        raise HTTPException(status_code=400, detail='Bad picked query-parameter')
    question = await apifunc.get_answer(id)
    return templates.TemplateResponse(
        'tiku/answer/main.jinja2', {
            'request': request,
            'current_user': current_user,
            'question': question,
            'picked': picked
        }
    )
