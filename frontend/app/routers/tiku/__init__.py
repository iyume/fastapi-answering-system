from typing import Any

from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import RedirectResponse

from .endpoints import area, paper, answer


router = APIRouter(prefix='/tiku')

router.include_router(area.router)   # /tiku/area
router.include_router(paper.router)  # /tiku/paper
router.include_router(answer.router) # /tiku/answer

@router.get('')
@router.get('/')
async def tiku_redirect(
    request: Request
) -> Any:
    return RedirectResponse(request.url_for('index'))
