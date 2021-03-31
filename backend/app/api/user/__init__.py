from fastapi import APIRouter

from . import user, extrapi
from .endpoints import answer_cache


router = APIRouter(prefix='/user', tags=['user'])

router.include_router(user.router)
router.include_router(answer_cache.router)
router.include_router(extrapi.router)
