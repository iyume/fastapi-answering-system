from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from app import crud
from app.api.auth import deps, authfunc
from app import schema


router = APIRouter()


@router.get('/')
async def list_users(
    uid: str = None,
    db: Session = Depends(deps.get_db)
) -> Any:
    if uid:
        user = crud.user.get_by_id(db, uid)
        return user
    result = crud.user.get_all(db)
    return result


@router.get('/done')
async def user_done_sample(
    username: str,
    db: Session = Depends(deps.get_db)
) -> Any:
    user = crud.user.get_by_name(db, username)
    return {
        "fb_done_count": user.fb_done_count,
        "fr_done_count": user.fr_done_count,
        "sr_done_count": user.sr_done_count
    }


@router.get('/exams')
async def user_all_exams(
    username: str,
    db: Session = Depends(deps.get_db)
) -> Any:
    results = crud.examquerycomplex.read_user_all_exams(db, username)
    return [
        {
            "exam_tag": result.tag,
            "start_time": result.start_time,
            "end_time": result.end_time,
            "exam_title": result.title,
            "exam_subject": result.subject,
            "exam_status": result.status
        }
        for result in results
    ]


@router.post('/change-password')
async def change_password(
    password_in: schema.UserChangePassword,
    db: Session = Depends(deps.get_db)
) -> Any:
    hashed_password = authfunc.encrypt_password(password_in.password_new)
    crud.user.update_password(db, password_in.uid, hashed_password)
    return 'success'


@router.post('/delete')
async def delete_user(
    uid: str,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    delete user by id
    """
    crud.user.delete(db, uid)
    return 'success'
