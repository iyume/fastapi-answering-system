from fastapi import APIRouter

from .endpoints import question, answer

api_router = APIRouter()

@api_router.on_event('startup')
async def startup():
    ...

@api_router.on_event('shutdown')
async def shutdown():
    ...

api_router.include_router(question.router, tags=['v1'])
api_router.include_router(answer.router, tags=['v1'])
