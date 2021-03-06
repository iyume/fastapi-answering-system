from typing import Optional, Any

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm.session import Session

from app import crud
from app.api import deps

router = APIRouter(prefix='/answer')

@router.get('/')
async def get_answer(
    id: str,
    db: Session = Depends(deps.get_db)
) -> Any:
    answer = crud.item.get_by_id(db, id=id)
    if not answer:
        raise HTTPException(status_code=400, detail='bad id')
    return answer
