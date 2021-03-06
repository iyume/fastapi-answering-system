import uuid
from typing import Optional, List

from sqlalchemy.orm import Session

from app.models.user import UserDB
from app.schema.user import UserCreate
from app.auth.func import encrypt_password


class CRUDUser():
    model = UserDB

    def get_by_id(
        self,
        db: Session,
        id: str
    ) -> Optional[UserDB]:
        return db.query(self.model).filter(self.model.id == id).first()

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
        obj_in: UserCreate,
        is_superuser: Optional[bool] = False
    ) -> Optional[UserDB]:
        db_obj = self.model(
            id = str(uuid.uuid4()),
            name = obj_in.name,
            email = obj_in.email,
            hashed_password = encrypt_password(obj_in.password),
            is_active = True,
            is_superuser = is_superuser
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        result = self.get_by_email(db, db_obj.email)
        return result

    def drop(
        self,
        db: Session,
        name: str
    ) -> str:
        user = db.query(self.model).filter(self.model.name == name).one()
        db.delete(user)
        db.commit()
        return 'success'


user = CRUDUser()
