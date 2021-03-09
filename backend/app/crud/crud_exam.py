from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import random

from app.models.exam import Exam, ExamInfo
from app import schema


class CRUDExamInfo():
    model = ExamInfo

    def fetchall(
        self,
        db: Session
    ) -> list[ExamInfo]:
        return db.query(self.model).all()

    def get_by_tag(
        self,
        db: Session,
        tag: str
    ) -> Optional[ExamInfo]:
        return db.query(self.model).filter(self.model.tag == tag).first()

    def create(
        self,
        db: Session,
        obj_in: schema.ExamCreate
    ) -> Optional[ExamInfo]:
        db_obj = self.model(
            tag = obj_in.tag,
            title = obj_in.title,
            detail = obj_in.detail,
            type = obj_in.type,
            subject = obj_in.subject,
            start_time = obj_in.start_time,
            end_time = obj_in.end_time
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(
        self,
        db: Session,
        tag: str
    ) -> None:
        exam = db.query(self.model).filter(self.model.tag == tag).first()
        if not exam:
            return None
        db.delete(exam)
        db.commit()


class CRUDExamCache():
    model = Exam


examinfo = CRUDExamInfo()
examcache = CRUDExamCache()
