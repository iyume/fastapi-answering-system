from fastapi import APIRouter

from .endpoints import question, answer, exam

api_router = APIRouter(tags=['v1'])

@api_router.on_event('startup')
async def startup() -> None:
    ...

@api_router.on_event('shutdown')
async def shutdown() -> None:
    ...

api_router.include_router(question.router)
api_router.include_router(answer.router)
api_router.include_router(exam.router)
