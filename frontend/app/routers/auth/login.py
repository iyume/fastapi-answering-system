from typing import Any, Optional
import time

from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse

from app.config import templates
from app.api import authfunc
from app import schema
from app.routers import deps
from app.models.user import UserPayload


router = APIRouter()


@router.get('/login', response_class=HTMLResponse)
async def login(
    request: Request,
    message: str = None,
    current_user: Optional[UserPayload] = Depends(deps.get_current_user)
) -> Any:
    if not current_user:
        return templates.TemplateResponse(
            'login/login.jinja2', {
                'request': request,
                'message': message
            }
        )
    if current_user.exp > time.time():
        return RedirectResponse(request.url_for('index'))


@router.post('/login', response_class=HTMLResponse)
async def login_action(
    request: Request,
    current_user: Optional[UserPayload] = Depends(deps.get_current_user)
) -> Any:
    if current_user:
        if current_user.exp > time.time():
            return RedirectResponse(request.url_for('index'))

    form = await request.form()
    if not (username := form.get('username', None)):
        return templates.TemplateResponse(
            'login/login.jinja2', {
                'request': request,
                'message': '请输入用户名'})
    if not (password := form.get('password', None)):
        return templates.TemplateResponse(
            'login/login.jinja2', {
                'request': request,
                'message': '请输入密码'})

    content = await authfunc.access_token(username, password)

    if isinstance(content, str):
        return RedirectResponse(
            request.url_for('login', message=content)
        )

    rr = RedirectResponse(request.url_for('tiku_area_index'), status_code=303)
    rr.set_cookie(
        key='jwt',
        value=content.access_token,
        httponly=True,
        samesite='strict')
    return rr
