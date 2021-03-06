from fastapi import APIRouter

from .endpoints import area, paper, answer


router = APIRouter(prefix='/tiku')

router.include_router(area.router)   # /tiku/area
router.include_router(paper.router)  # /tiku/paper
router.include_router(answer.router) # /tiku/answer
