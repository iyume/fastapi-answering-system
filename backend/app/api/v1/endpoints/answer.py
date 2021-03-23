from typing import Optional, Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from app import crud, schema
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


@router.post('/many')
async def get_answer_many(
    id_list_obj: schema.ItemIdMany,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    get question by id list, only return question_id with question_answer
    """
    results = crud.item.get_by_id_many(db, id_list_obj)
    return [
        {
            "question_id": result.id,
            "answer": result.answer
        }
        for result in results
    ]
