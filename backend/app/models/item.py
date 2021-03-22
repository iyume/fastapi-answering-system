from sqlalchemy import Column, String, Integer

from app.db.base_class import Base


class Item(Base):
    __tablename__ = 'questions'

    id = Column('id', String(36), primary_key=True)
    question = Column('q', String(500))
    option_a = Column('a', String(100))
    option_b = Column('b', String(100))
    option_c = Column('c', String(100))
    option_d = Column('d', String(100))
    answer = Column('answer', String(1))
    knowledge_point = Column('knowledge_point', String(80))
    question_type = Column('question_type', String(10))
    difficulty = Column('difficulty', String(10))
    year = Column('year', Integer)
    subject = Column('subject', String(10))

class ItemCache(Base):
    __tablename__ = 'answer_cache'

    username = Column(String(16))
    question_id = Column(String(36))
    picked = Column(String(1))
    fade_key = Column(Integer, primary_key=True, autoincrement=True)
