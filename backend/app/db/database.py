import os
from databases import Database

from app.config import config

database = Database(config.DATABASE_URI)
