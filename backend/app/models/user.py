from typing import Optional
from datetime import datetime

from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.orm import relationship

from app import crud
from app.auth import deps, authfunc
from app.db.base_class import Base


class UserDB(Base):
    __tablename__ = 'user'

    id = Column('id', String(60), primary_key=True)
    name = Column('name', String(16))
    email = Column('email', String(254), unique=True)
    wechat = Column('wechat', String(16))
    hashed_password = Column('hashed_password', String(60), nullable=False)
    is_active = Column('is_active', Boolean, default=True)
    is_superuser = Column('is_superuser', Boolean, default=False)
    created_time = Column('created_time', DateTime, default=datetime.now())
    first_login = Column('first_login', DateTime)
    exam = relationship('ExamCache')    

    def validate_password(self, password: str) -> bool:
        return authfunc.verify_password(password, self.hashed_password)


class User():
    # temporary the implement in flask
    def __init__(self, name: str, password: Optional[str] = None) -> None:
        db = next(deps.get_db())
        self.current_user = crud.user.get_by_name(db, name)
        if password:
            self.is_authenticated = self.validate_password(password)

    def validate_password(self, plain_password: str) -> bool:
        if not self.current_user:
            return False
        if not self.hashed_password:
            return False
        return authfunc.verify_password(plain_password, self.hashed_password)

    @property
    def id(self) -> Optional[str]:
        return getattr(self.current_user, 'id', None)

    @property
    def name(self) -> Optional[str]:
        return getattr(self.current_user, 'name', None)

    @property
    def email(self) -> Optional[str]:
        return getattr(self.current_user, 'email', None)

    @property
    def wechat(self) -> Optional[str]:
        return getattr(self.current_user, 'wechat', None)

    @property
    def hashed_password(self) -> Optional[str]:
        return getattr(self.current_user, 'hashed_password', None)

    @property
    def is_active(self) -> bool:
        return getattr(self.current_user, 'is_active', True)

    @property
    def is_superuser(self) -> bool:
        return getattr(self.current_user, 'is_superuser', False)
