from typing import Generator

from app.db.load_db import SessionMaker

def get_db() -> Generator:
    try:
        db = SessionMaker()
        yield db
    finally:
        db.close()
