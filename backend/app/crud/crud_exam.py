from typing import Optional, Union

from sqlalchemy.orm import Session

from app.models.exam import ExamCache, ExamInfo, ExamStatus
from app.models.user import UserDB
from app import schema


class CRUDExamInfo():
    model = ExamInfo

    def fetchall(
        self,
        db: Session
    ) -> list[ExamInfo]:
        return db.query(self.model).order_by(self.model.created_time.desc()).all()

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
        examstatus.create_all(db, obj_in.tag)
        return self.get_by_tag(db, obj_in.tag)

    def update(
        self,
        db: Session,
        obj_in: schema.ExamUpdate
    ) -> None:
        (db
        .query(self.model)
        .filter(self.model.tag == obj_in.tag)
        .update(dict(obj_in))
        )
        db.commit()

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
        examstatus.delete_all(db, exam_tag=tag)


class CRUDExamCache():
    model = ExamCache

    def create_paper(
        self,
        db: Session,
        obj_in: schema.ExamBase,
        question_id_list: list[str]
    ) -> None:
        db_obj_list = []
        for i in range(len(question_id_list)):
            db_obj_list.append(self.model(
                user_id = obj_in.user_id,
                exam_tag = obj_in.exam_tag,
                question_id = question_id_list[i],
                question_order = i + 1
            ))
        db.add_all(db_obj_list)
        db.commit()
        for i in db_obj_list:
            db.refresh(i)
        return None

    def paper_status(
        self,
        db: Session,
        obj_in: schema.ExamBase
    ) -> Optional[ExamStatus]:
        return examstatus.query_status(db, obj_in)

    def finish_paper(
        self,
        db: Session,
        obj_in: schema.ExamStatusUpdate
    ) -> None:
        examstatus.update(db, obj_in)

    def fetchone(
        self,
        db: Session,
        obj_in: schema.ExamBase
    ) -> Optional[ExamCache]:
        return (
            db.query(self.model)
            .filter(self.model.user_id == obj_in.user_id)
            .filter(self.model.exam_tag == obj_in.exam_tag)
            .first()
        )

    def get_by_condition(
        self,
        db: Session,
        obj_in: schema.ExamPaperQuery
    ) -> Union[ExamCache, list[ExamCache], None]:
        if obj_in.question_order:
            return (
                db.query(self.model)
                .filter(self.model.user_id == obj_in.user_id)
                .filter(self.model.exam_tag == obj_in.exam_tag)
                .filter(self.model.question_order == obj_in.question_order)
                .first()
            )
        return (
            db.query(self.model)
            .filter(self.model.user_id == obj_in.user_id)
            .filter(self.model.exam_tag == obj_in.exam_tag)
            .all()
        )

    def get_first_not_picked(
        self,
        db: Session,
        obj_in: schema.ExamBase
    ) -> Optional[ExamCache]:
        return (
            db.query(self.model)
            .filter(self.model.user_id == obj_in.user_id)
            .filter(self.model.exam_tag == obj_in.exam_tag)
            .filter(self.model.picked != None)
            .first()
        )

    def update_picked(
        self,
        db: Session,
        obj_in: schema.ExamPaperUpdate
    ) -> None:
        (db
        .query(self.model)
        .filter(self.model.user_id == obj_in.user_id)
        .filter(self.model.exam_tag == obj_in.exam_tag)
        .filter(self.model.question_id == obj_in.question_id)
        .update({self.model.picked: obj_in.picked})
        )
        db.commit()

    def delete_exam_cache(
        self,
        db: Session,
        exam_tag: str
    ) -> None:
        db.query(self.model).filter(self.model.exam_tag == exam_tag).delete()
        db.commit()


class CRUDExamStatus():
    model = ExamStatus

    def create_all(
        self,
        db: Session,
        exam_tag: str
    ) -> None:
        users = db.query(UserDB).all()
        db_obj_list = []
        for user in users:
            db_obj_list.append(self.model(
                user_id = user.id,
                exam_tag = exam_tag
            ))
        db.add_all(db_obj_list)
        db.commit()
        for i in db_obj_list:
            db.refresh(i)
        return None

    def create(
        self,
        db: Session,
        obj_in: schema.ExamBase
    ) -> None:
        exam_status = self.model(user_id = obj_in.user_id, exam_tag = obj_in.exam_tag)
        db.add(exam_status)
        db.commit()
        db.refresh(exam_status)

    def query_all(
        self,
        db: Session
    ) -> list[ExamStatus]:
        return db.query(self.model).order_by(self.model.fade_key.desc()).all()

    def query_user_all(
        self,
        db: Session,
        user_id: str
    ) -> list[ExamStatus]:
        return (
            db.query(self.model)
            .filter(self.model.user_id == user_id)
            .order_by(self.model.fade_key.desc())
            .all()
        )

    def query_status(
        self,
        db: Session,
        obj_in: schema.ExamBase
    ) -> Optional[ExamStatus]:
        return (
            db.query(self.model)
            .filter(self.model.user_id == obj_in.user_id)
            .filter(self.model.exam_tag == obj_in.exam_tag)
            .first()
        )

    def update(
        self,
        db: Session,
        obj_in: schema.ExamStatusUpdate
    ) -> None:
        (db
        .query(self.model)
        .filter(self.model.user_id == obj_in.user_id)
        .filter(self.model.exam_tag == obj_in.exam_tag)
        .update({self.model.status: obj_in.status})
        )
        db.commit()

    def delete(
        self,
        db: Session,
        obj_in: schema.ExamBase
    ) -> None:
        db_exam_status = (db
        .query(self.model)
        .filter(self.model.user_id == obj_in.user_id)
        .filter(self.model.exam_tag == obj_in.exam_tag)
        .first()
        )
        db.delete(db_exam_status)
        db.commit()

    def delete_all(
        self,
        db: Session,
        exam_tag: str
    ) -> None:
        db_list = db.query(self.model).filter(self.model.exam_tag == exam_tag).delete()
        db.commit()

    def delete_by_fadekey(
        self,
        db: Session,
        fade_key: int
    ) -> None:
        db_exam_status = db.query(self.model).filter(self.model.fade_key == fade_key).first()
        db.delete(db_exam_status)
        db.commit()


examinfo = CRUDExamInfo()
examcache = CRUDExamCache()
examstatus = CRUDExamStatus() # only for extrapi
