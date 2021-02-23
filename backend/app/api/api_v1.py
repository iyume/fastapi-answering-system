from fastapi import APIRouter

from .v1.router import api_router

router = APIRouter(prefix='/api')

router.include_router(api_router, prefix='/v1')
