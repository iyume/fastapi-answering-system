from app import crud
from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from app.api import deps

router = APIRouter(prefix='/answer')

@router.get('/')
async def get_answer(
    db: Session = Depends(deps.get_db),
    id: Optional[str] = None
):
    if not id:
        return None
    answer = crud.item.get_by_id(db, id=id)
    return answer
