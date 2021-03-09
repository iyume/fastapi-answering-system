from fastapi import APIRouter

from . import crud_exam


router = APIRouter(prefix='/manager')

router.include_router(crud_exam.router)
