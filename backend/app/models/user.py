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
            self.is_authenticated = self.validate_password(password)

    def validate_password(self, plain_password: str) -> bool:
        if not self.current_user:
            return False
        return func.verify_password(plain_password, self.hashed_password)

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
