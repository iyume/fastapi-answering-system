from typing import Any

from fastapi import APIRouter, Depends
from starlette.requests import Request

from app.config import templates
from app.security import login_required
from app.routers import deps
from app import schema


router = APIRouter()


@router.get('/entry')
@login_required
async def exam_entry(
    request: Request,
    current_user: schema.UserPayload = Depends(deps.get_current_user)
) -> Any:
    return templates.TemplateResponse(
        'exam/entry.jinja2', {
            'request': request,
            'current_user': current_user
        }
    )
