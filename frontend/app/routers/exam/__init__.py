from fastapi import APIRouter

from . import exam


router = APIRouter(prefix='/exam')

router.include_router(exam.router)
