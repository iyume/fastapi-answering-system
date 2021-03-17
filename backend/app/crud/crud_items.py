from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import random

from app.models.item import Item
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


item = CRUDQuestion()
