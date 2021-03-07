from pydantic import BaseModel


class JWT(BaseModel):
    access_token: str
    exp: int

class Secret(BaseModel):
    secret: str
