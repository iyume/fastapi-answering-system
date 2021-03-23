from fastapi import APIRouter

from . import auth, extrapi


router = APIRouter(prefix='/auth', tags=['auth'])

router.include_router(auth.router)
router.include_router(extrapi.router)
