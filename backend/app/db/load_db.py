from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

from app.config import config

engine = create_engine(config.DATABASE_URI)
SessionMaker = sessionmaker(autocommit=False, autoflush=False, bind=engine)
