import uuid
from typing import Optional

from sqlalchemy.orm import Session

from app.models.user import UserDB
from app.schema.user import UserCreate
from app.auth.func import encrypt_password


class CRUDUser():
    model = UserDB

    def get_by_name(
        self,
        db: Session,
        name: str
    ) -> Optional[model]:
        return db.query(self.model).filter(self.model.name == name).first()

    def get_by_email(
        self,
        db: Session,
        email: str
    ) -> Optional[model]:
        return db.query(self.model).filter(self.model.email == email).first()

    def create(
        self,
        db: Session,
        obj_in: UserCreate,
        is_superuser: Optional[bool] = False
    ) -> Optional[model]:
        if result := self.get_by_email(db, obj_in.email):
            return result
        else:
            db_obj = self.model(
                id = str(uuid.uuid4()),
                name = obj_in.name,
                email = obj_in.email,
                hashed_password = encrypt_password(obj_in.password),
                is_superuser = is_superuser
            )
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            result = self.get_by_email(db, db_obj.email)
            return db_obj


user = CRUDUser()
