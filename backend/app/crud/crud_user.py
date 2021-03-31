import uuid
from datetime import datetime
from typing import Optional, List

from sqlalchemy.orm import Session

from app.models.user import UserDB
from app import schema


class CRUDUser():
    model = UserDB

    def get_by_id(
        self,
        db: Session,
        uid: str
    ) -> Optional[UserDB]:
        return db.query(self.model).filter(self.model.id == uid).first()

    def get_by_name(
        self,
        db: Session,
        name: str
    ) -> Optional[UserDB]:
        return db.query(self.model).filter(self.model.name == name).first()

    def get_by_email(
        self,
        db: Session,
        email: str
    ) -> Optional[UserDB]:
        return db.query(self.model).filter(self.model.email == email).first()

    def get_all(
        self,
        db: Session
    ) -> List[UserDB]:
        return db.query(self.model).all()

    def create(
        self,
        db: Session,
        obj_in: schema.UserCreate,
        is_superuser: Optional[bool] = False
    ) -> Optional[UserDB]:
        db_obj = self.model(
            id = str(uuid.uuid4()),
            name = obj_in.name,
            email = obj_in.email,
            hashed_password = obj_in.hashed_password,
            is_active = True,
            is_superuser = is_superuser,
            created_time = datetime.now()
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        result = self.get_by_id(db, db_obj.id)
        return result

    def update_first_login(
        self,
        db: Session,
        uid: str
    ) -> None:
        (db
        .query(self.model)
        .filter(self.model.id == uid)
        .update({self.model.first_login: datetime.now()})
        )
        db.commit()

    def update_password(
        self,
        db: Session,
        uid: str,
        hashed_password: str
    ) -> None:
        (db
        .query(self.model)
        .filter(self.model.id == uid)
        .update({self.model.hashed_password: hashed_password})
        )
        db.commit()

    def update_recent_done_exam(
        self,
        db: Session,
        username: str,
        exam_tag: str
    ) -> None:
        (db
        .query(self.model)
        .filter(self.model.name == username)
        .update({self.model.recent_done_exam: exam_tag})
        )
        db.commit()

    def update_done_counter(
        self,
        db: Session,
        username: str,
        fb_done_count: int,
        fr_done_count: int,
        sr_done_count: int
    ) -> None:
        (db
        .query(self.model)
        .filter(self.model.name == username)
        .update({
            self.model.fb_done_count: fb_done_count,
            self.model.fr_done_count: fr_done_count,
            self.model.sr_done_count: sr_done_count})
        )
        db.commit()


    def delete(
        self,
        db: Session,
        uid: str
    ) -> None:
        user = db.query(self.model).filter(self.model.id == uid).one()
        db.delete(user)
        db.commit()


user = CRUDUser()
