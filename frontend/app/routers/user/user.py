from typing import Any

from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.config import templates
from app.routers import deps
from app import schema
from app.security.func import login_required


router = APIRouter()


@router.get('/{username}')
@login_required
async def homepage(
    request: Request,
    username: str,
    current_user: schema.UserDetail = Depends(deps.get_current_user_detail)
) -> Any:
    if current_user.name == username:
        return templates.TemplateResponse(
            'user/homepage.jinja2', {
                'request': request,
                'current_user': current_user
            }
        )
    return RedirectResponse(request.url_for('index'))
