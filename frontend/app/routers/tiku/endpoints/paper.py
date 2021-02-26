from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from starlette.requests import Request
from starlette.responses import HTMLResponse

from app.config import templates
from app.api import question_random

router = APIRouter(prefix='/paper')

info = {
    'fb': {
        'name': '基金基础'
    },
    'fr': {},
    'sr': {}
}

@router.get('/fb', response_class=HTMLResponse)
async def tiku_paper_fb(request: Request, type: str):
    if type == 'random':
        question = await question_random('fb')
        return templates.TemplateResponse(
            'tiku/paper/fb.jinja2', {
                'request': request,
                'question': question
            }
        )
    else:
        return RedirectResponse(request.url_for('tiku_area_fb'))

@router.get('/fr', response_class=HTMLResponse)
async def tiku_paper_fr(request: Request, type: str):
    return templates.TemplateResponse(
        'tiku/paper/fr.jinja2', {
            'request': request
        }
    )

@router.get('/sr', response_class=HTMLResponse)
async def tiku_paper_sr(request: Request, type: str):
    return templates.TemplateResponse(
        'tiku/paper/sr.jinja2', {
            'request': request
        }
    )
