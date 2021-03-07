from typing import Any

from fastapi import APIRouter


router = APIRouter()


@router.get('')
@router.get('/')
async def exam() -> Any:
    ...
