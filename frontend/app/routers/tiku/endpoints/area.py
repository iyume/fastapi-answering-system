from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse

from app.config import templates

router = APIRouter(prefix='/area')

@router.get('/', response_class=HTMLResponse)
async def tiku_area_index(request: Request):
    return templates.TemplateResponse('tiku/area/index.jinja2' ,{'request': request})

@router.get('/fb', response_class=HTMLResponse)
async def tiku_area_fb(request: Request):
    return templates.TemplateResponse('tiku/area/fb.jinja2' ,{'request': request})

@router.get('/fr', response_class=HTMLResponse)
async def tiku_area_fr(request: Request):
    return templates.TemplateResponse('tiku/area/fr.jinja2' ,{'request': request})

@router.get('/sr', response_class=HTMLResponse)
async def tiku_area_sr(request: Request):
    return templates.TemplateResponse('tiku/area/sr.jinja2' ,{'request': request})
