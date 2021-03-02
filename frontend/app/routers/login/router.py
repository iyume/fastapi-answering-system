from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse

from app.config import templates
from app.api import authfunc
from app.schema.token import Token


login_router = APIRouter(prefix='/login')


@login_router.get('/', response_class=HTMLResponse)
async def login(request: Request):
    form = await request.form()
    return templates.TemplateResponse('login/login.jinja2', {'request': request})

@login_router.post('/', response_class=HTMLResponse)
async def login_action(request: Request):
    form = await request.form()
    if not (username := form.get('username', None)):
        return templates.TemplateResponse(
            'login/login.jinja2',
            {
                'request': request,
                'message': '请输入用户名'
            }
        )
    if not (password := form.get('password', None)):
        return templates.TemplateResponse(
            'login/login.jinja2',
            {
                'request': request,
                'message': '请输入密码'
            }
        )
    content = await authfunc.authenticate(username, password)
    if isinstance(content, str):
        return templates.TemplateResponse(
            'login/login.jinja2',
            {
                'request': request,
                'message': content
            }
        )
    if isinstance(content, Token):
        return content.token
