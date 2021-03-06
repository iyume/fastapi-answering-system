from sqlalchemy import Column, String

from app.db.base_class import Base


class Item(Base):
    __tablename__ = 'questions'

    id = Column('id', String, primary_key=True)
    question = Column('q', String)
    option_a = Column('a', String)
    option_b = Column('b', String)
    option_c = Column('c', String)
    option_d = Column('d', String)
    answer = Column('answer', String)
    knowledge_point = Column('knowledge_point', String)
    question_type = Column('question_type', String)
    difficulty = Column('difficulty', String)
    year = Column('year', String)
    subject = Column('subject', String)
