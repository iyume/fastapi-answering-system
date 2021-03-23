from fastapi import APIRouter

from . import user


router = APIRouter(prefix='/user', tags=['user'])

router.include_router(user.router)
