from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import random

from app.models.item import Item


class CRUDQuestion():
    def get_by_random(
        self,
        db: Session,
        subject: Optional[str] = None
    ) -> Optional[Item]:
        if subject:
            return db.query(Item).filter(Item.subject == subject).order_by(random()).first()
        else:
            return db.query(Item).order_by(random()).first()

    def get_by_id(
        self,
        db: Session,
        id: str
    ) -> Optional[Item]:
        return db.query(Item).filter(Item.id == id).first()


item = CRUDQuestion()
