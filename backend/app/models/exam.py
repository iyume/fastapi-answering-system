from sqlalchemy import Column, String, TIMESTAMP, ForeignKey
from sqlalchemy.sql.functions import now

from app.db.base_class import Base


class ExamInfo(Base):
    __tablename__ = 'exam_info'

    tag = Column('tag', String(10), primary_key=True)
    title = Column('title', String(20), nullable=False)
    detail = Column('detail', String(200))
    type = Column('type', String(10))
    created_time = Column('created_time', TIMESTAMP, default=now())
    start_time = Column('start_time', TIMESTAMP, nullable=False)
    end_time = Column('end_time', TIMESTAMP, nullable=False)

class Exam(Base):
    __tablename__ = 'exam'

    user_id = Column(String(36), ForeignKey('user.id'))
    question_id = Column(String(36), ForeignKey('questions.id'))
    picked = Column(String(1))
    exam_tag = Column(String(10), ForeignKey('exam.tag'))
    fade_key = Column(String(36), primary_key=True)
