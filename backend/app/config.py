import os


class Config():
    __name__ = 'config'

    @property
    def DATABASE_URI(self):
        current_path = os.path.dirname(os.path.realpath(__file__))
        db_name = 'db/all.db'
        return f'sqlite:///{os.path.join(current_path, db_name)}'

config = Config()
