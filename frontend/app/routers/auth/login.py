from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse

from app.config import templates
from app.api import authfunc
from app.schema import Token


router = APIRouter()


@router.get('/login', response_class=HTMLResponse)
async def login(request: Request):
    form = await request.form()
    return templates.TemplateResponse('login/login.jinja2', {'request': request})

@router.post('/login', response_class=HTMLResponse)
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
        rr = RedirectResponse(request.url_for('tiku_area_index'), status_code=303)
        rr.set_cookie(key='jwt', value=content.access_token)
        return rr
    raise HTTPException(status_code=400, detail='Bad request')
