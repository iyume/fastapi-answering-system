from typing import Optional

from sqlalchemy import Column, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

from app import crud
from app.auth import deps, func


Base = declarative_base()

class UserDB(Base):
    __tablename__ = 'user'

    id = Column('id', String, primary_key=True)
    name = Column('name', String)
    email = Column('email', String)
    wechat = Column('wechat', String)
    hashed_password = Column('hashed_password', String)
    is_active = Column('is_active', Boolean)
    is_superuser = Column('is_superuser', Boolean)


class User():
    def __init__(self, name: str, password: Optional[str] = None) -> None:
        db = next(deps.get_db())
        self.current_user = crud.user.get_by_name(db, name)
        if password:
            self.is_authenticated = self.validate_user(password)

    def validate_user(self, plain_password: str) -> bool:
        return func.verify_password(plain_password, self.hashed_password)

    @property
    def name(self) -> str:
        return self.current_user.name

    @property
    def email(self) -> str:
        return self.current_user.email

    @property
    def wechat(self) -> str:
        return self.current_user.wechat

    @property
    def hashed_password(self) -> str:
        return self.current_user.hashed_password

    @property
    def is_active(self) -> bool:
        return self.current_user.is_active or True

    @property
    def is_superuser(self) -> bool:
        return self.current_user.is_superuser or False
