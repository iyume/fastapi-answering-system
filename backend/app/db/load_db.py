from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import config

engine = create_engine(
    config.DATABASE_URI,
    echo=False,
    connect_args={
        'check_same_thread': False
    }
)

SessionMaker = sessionmaker(autocommit=False, autoflush=False, bind=engine)
