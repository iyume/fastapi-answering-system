from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import random

from app.models.exam import Exam, ExamInfo
from app import schema


class CRUDExamInfo():
    model = ExamInfo

    def create(
        self,
        db: Session,
        obj_in: schema.ExamCreate
    ) -> Optional[ExamInfo]:
        ...


class CRUDExamCache():
    model = Exam


class CRUDExam(CRUDExamInfo, CRUDExamCache):
    ...


exam = CRUDExam()
