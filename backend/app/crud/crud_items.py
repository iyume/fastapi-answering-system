from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import random

from app.models.questions import Questions


class CRUDQuestion():
    def get_by_random(self, db: Session) -> Optional[Questions]:
        return db.query(Questions).order_by(random()).first()

    def get_by_id(self, db: Session, id: str) -> Optional[Questions]:
        return db.query(Questions).filter(Questions.id==id).first()

item = CRUDQuestion()
