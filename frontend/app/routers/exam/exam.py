from typing import Any
from datetime import datetime

from fastapi import APIRouter, Depends
from starlette.requests import Request

from app.config import templates
from app.security import login_required
from app.routers import deps
from app import schema
from app.api import apifunc


router = APIRouter()


@router.get('/entry')
@login_required
async def exam_entry(
    request: Request,
    current_user: schema.UserPayload = Depends(deps.get_current_user)
) -> Any:
    exams = await apifunc.exam_fetchall()
    unstarted_exams: list[dict] = []
    processing_exams: list[dict] = []
    finished_exams: list[dict] = []
    for exam in exams:
        exam['start_time'] = datetime.fromisoformat(exam['start_time'])
        exam['end_time'] = datetime.fromisoformat(exam['end_time'])
        if exam['start_time'] > datetime.now():
            unstarted_exams.append(exam)
        if exam['end_time'] < datetime.now():
            finished_exams.append(exam)
        if exam['start_time'] < datetime.now() < exam['end_time']:
            processing_exams.append(exam)
    for exam in exams:
        exam['start_time'] = datetime.strftime(exam['start_time'], '%F %X')
        exam['end_time'] = datetime.strftime(exam['end_time'], '%F %X')
    return templates.TemplateResponse(
        'exam/entry.jinja2', {
            'request': request,
            'current_user': current_user,
            'unstarted_exams': unstarted_exams,
            'processing_exams': processing_exams,
            'finished_exams': finished_exams
        }
    )
