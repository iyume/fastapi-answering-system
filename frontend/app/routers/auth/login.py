import time
from typing import Any

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
    current_user: UserPayload = Depends(deps.get_current_user)
) -> Any:
    if current_user.exp > time.time():
        return RedirectResponse(request.url_for('index'))
    return templates.TemplateResponse('login/login.jinja2', {'request': request})


@router.post('/login', response_class=HTMLResponse)
async def login_action(
    request: Request,
    current_user: UserPayload = Depends(deps.get_current_user)
) -> Any:
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

    jwt: schema.JWT = await authfunc.authenticate(username, password)
    rr = RedirectResponse(request.url_for('tiku_area_index'), status_code=303)
    rr.set_cookie(key='jwt', value=jwt.access_token)
    return rr
