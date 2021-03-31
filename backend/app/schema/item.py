from typing import Optional

from pydantic import BaseModel


class ItemIdMany(BaseModel):
    id_list: list[str]


class ItemCacheBase(BaseModel):
    username: str

class ItemCacheCreate(ItemCacheBase):
    question_id: str
    picked: str
    paper_type: str
    subject: str # for userinfo increase counter
