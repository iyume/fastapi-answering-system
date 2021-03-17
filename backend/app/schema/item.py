from typing import Optional

from pydantic import BaseModel


class ItemIdMany(BaseModel):
    id_list: list[str]
