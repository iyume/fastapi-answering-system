from fastapi import APIRouter

from . import crud_exam, crud_account, user_activity


router = APIRouter(prefix='/manager')

router.include_router(crud_exam.router)
router.include_router(crud_account.router)
router.include_router(user_activity.router)
