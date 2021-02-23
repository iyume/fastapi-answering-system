import os

from databases import Database

current_path = os.path.dirname(os.path.realpath(__file__))
db_name = 'questions.db'
db_path = os.path.join(current_path, db_name)
database = Database(f'sqlite:///{db_path}')
