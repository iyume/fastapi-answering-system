from typing import Any, Generator

from app.db.load_db import SessionMaker

def get_db() -> Generator:
    db: Any = None # escape pylance
    try:
        db = SessionMaker()
        yield db
    finally:
        db.close()
