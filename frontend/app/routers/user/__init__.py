from fastapi import APIRouter

from . import user


router = APIRouter(prefix='/user')

router.include_router(user.router)
