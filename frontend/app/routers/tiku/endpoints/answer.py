from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from starlette.requests import Request
from starlette.responses import HTMLResponse

from app.config import templates
from app.api import get_answer

router = APIRouter(prefix='/answer')

@router.get('/fb', response_class=HTMLResponse)
async def tiku_answer_fb(request: Request, id: str, answer: str):
    question = await get_answer(subject='fb', id=id)
    return templates.TemplateResponse('tiku/answer/fb.jinja2' ,{'request': request, 'question': question, 'answer': answer})

@router.post('/fr', response_class=HTMLResponse)
async def tiku_paper_fr(request: Request, type: str):
    return templates.TemplateResponse('tiku/paper/fr.jinja2' ,{'request': request})

@router.post('/sr', response_class=HTMLResponse)
async def tiku_paper_sr(request: Request, type: str):
    return templates.TemplateResponse('tiku/paper/sr.jinja2' ,{'request': request})
