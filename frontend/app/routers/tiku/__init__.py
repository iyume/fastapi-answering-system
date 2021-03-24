from typing import Any

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.security import login_required
from app.models import UserPayload
from app.routers import deps

from . import area, paper, answer


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

@router.post('/order-refresh/{subject}')
@login_required
async def paper_order_refresh(
    request: Request,
    subject: str,
    current_user: UserPayload = Depends(deps.get_current_user)
) -> Any:
    raise HTTPException(status_code=200, detail='进行中的工作')
