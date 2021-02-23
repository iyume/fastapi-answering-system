from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse

from app.config import templates

login_router = APIRouter(prefix='/login')

@login_router.get('/', response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse('login/login.jinja2', {'request': request})
