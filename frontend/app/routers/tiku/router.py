from fastapi import APIRouter

from .endpoints import area, paper, answer

tiku_router = APIRouter(prefix='/tiku')

tiku_router.include_router(area.router)   # /tiku/area
tiku_router.include_router(paper.router)  # /tiku/paper
tiku_router.include_router(answer.router) # /tiku/answer
