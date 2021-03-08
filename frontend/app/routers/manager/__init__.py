from fastapi import APIRouter

from . import super


router = APIRouter(prefix='/manager')

router.include_router(super.router)
