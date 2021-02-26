from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class FB(Base):
    __tablename__ = '基金基础'

    id = Column(String)
    q = Column('问题', String)
    a = Column('A', String)
    b = Column('B', String)
    c = Column('C', String)
    d = Column('D', String)
    answer = Column('答案', String)

