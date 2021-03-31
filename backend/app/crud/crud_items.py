from typing import Optional
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import random

from app.models.item import Item, ItemCache
from app.models.user import UserDB
from app import schema


class CRUDQuestion():
    model = Item

    def get_by_random(
        self,
        db: Session,
        subject: Optional[str] = None
    ) -> Optional[Item]:
        if subject:
            return (
                db.query(self.model)
                .filter(self.model.subject == subject)
                .order_by(random())
                .first()
            )
        return db.query(self.model).order_by(random()).first()

    def get_by_random_many(
        self,
        db: Session,
        amount: int,
        subject: Optional[str] = None
    ) -> list[Item]:
        if subject:
            return (
                db.query(self.model)
                .filter(self.model.subject == subject)
                .order_by(random())
                .limit(amount)
                .all()
            )
        return db.query(self.model).order_by(random()).limit(amount).all()

    def get_by_id(
        self,
        db: Session,
        id: str
    ) -> Optional[Item]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_by_id_many(
        self,
        db: Session,
        obj_in: schema.ItemIdMany
    ) -> list[Item]:
        return db.query(self.model).filter(self.model.id.in_(obj_in.id_list)).all()

    def get_by_subject_order(
        self,
        db: Session,
        subject: str,
        order: int
    ) -> Optional[Item]:
        return (
            db.query(self.model)
            .filter(self.model.subject == subject)
            .offset(order-1)
            .first()
        )

    def get_by_subject_all(
        self,
        db: Session,
        subject: str
    ) -> list[Item]:
        return db.query(self.model).filter(self.model.subject == subject).all()


class CRUDItemCache():
    model = ItemCache

    def create(
        self,
        db: Session,
        obj_in: schema.ItemCacheCreate,
    ) -> None:
        if not db.query(self.model).filter(self.model.question_id == obj_in.question_id).first():
            # increase amount of question in userinfo
            db_obj = db.query(UserDB).filter(UserDB.name == obj_in.username).first()
            if obj_in.subject == 'fb':
                update_dict = {UserDB.fb_done_count: db_obj.fb_done_count + 1}
            elif obj_in.subject == 'fr':
                update_dict = {UserDB.fr_done_count: db_obj.fr_done_count + 1}
            elif obj_in.subject == 'sr':
                update_dict = {UserDB.sr_done_count: db_obj.sr_done_count + 1}
            else:
                raise HTTPException(status_code=400, detail='invalid subject in creating answer cache')
            db.query(UserDB).filter(UserDB.name == obj_in.username).update(update_dict)
            db.commit()
        db_obj = self.model(
            username = obj_in.username,
            question_id = obj_in.question_id,
            picked = obj_in.picked,
            paper_type = obj_in.paper_type,
            created_time = datetime.now()
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

    def query_userall(
        self,
        db: Session,
        username: str
    ) -> list[ItemCache]:
        return (
            db.query(self.model)
            .filter(self.model.username == username)
            .all()
        )

    def query_userall_unique(
        self,
        db: Session,
        username: str,
        is_fresh: bool = True
    ) -> list[dict]:
        if is_fresh:
            db_objs = (
                db.query(self.model)
                .filter(self.model.username == username)
                .filter(self.model.refreshed == False)
                .filter(self.model.paper_type == 'order')
                .all()
            )
        else:
            db_objs = (
                db.query(self.model)
                .filter(self.model.username == username)
                .filter(self.model.paper_type == 'order')
                .all()
            )
        qid_set = set()
        results = []
        while db_objs:
            handler = db_objs[-1]
            if handler.question_id not in qid_set:
                qid_set.add(handler.question_id)
                results.append(handler)
                db_objs.pop()
            else:
                db_objs.pop()
        return results

    def refresh(
        self,
        db: Session,
        username: str
    ) -> None:
        (db
        .query(self.model)
        .filter(self.model.username == username)
        .update({self.model.refreshed: True})
        )
        db.commit()


item = CRUDQuestion()
itemcache = CRUDItemCache()
