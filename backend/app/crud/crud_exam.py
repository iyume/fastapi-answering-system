from typing import Optional
from random import randint

from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import random

from app.models.exam import ExamCache, ExamInfo
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
            question_count = obj_in.question_count,
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
    model = ExamCache

    def create_paper(
        self,
        db: Session,
        user_id: str,
        exam_tag: str,
        question_id_list: list[str]
    ) -> None:
        db_obj_list = []
        for i in range(len(question_id_list)):
            db_obj_list.append(self.model(
                user_id = user_id,
                question_id = question_id_list[i],
                exam_tag = exam_tag,
                question_order = i + 1
            ))
        db.add_all(db_obj_list)
        db.commit()
        for i in db_obj_list:
            db.refresh(i)
        return None

    def fetchone(
        self,
        db: Session,
        user_id: str,
        exam_tag: str,
    ) -> Optional[ExamCache]:
        return (
            db.query(self.model)
            .filter(self.model.user_id == user_id)
            .filter(self.model.exam_tag == exam_tag)
            .first()
        )


examinfo = CRUDExamInfo()
examcache = CRUDExamCache()
