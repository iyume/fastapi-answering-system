from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.sql.sqltypes import Integer

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
    created_time = Column('created_time', DateTime, nullable=False)
    first_login = Column('first_login', DateTime)

    fb_done_count = Column(Integer, default=0)
    fr_done_count = Column(Integer, default=0)
    sr_done_count = Column(Integer, default=0)
    recent_done_exam = Column(String(20))
