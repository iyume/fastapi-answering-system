from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class ExamCreate(BaseModel):
    tag: str
    title: str
    detail: Optional[str] = None
    type: str
    subject: str
    question_count: int
    start_time: datetime
    end_time: datetime
