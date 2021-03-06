from typing import Optional, Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from app import crud
from app.api import deps

router = APIRouter(prefix='/answer')

@router.get('/')
async def get_answer(
    id: str,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    get question by id, call it `get_answer` for its usage
    """
    answer = crud.item.get_by_id(db, id=id)
    return answer
