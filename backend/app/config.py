import os
import pretty_errors

pretty_errors.replace_stderr()

class Config():
    __name__ = 'config'

    db_dir = 'db'
    db_name = 'all.db'

    @property
    def CURRENT_PATH(self):
        return os.path.dirname(os.path.realpath(__file__))

    @property
    def DATABASE_URI(self):
        return f'sqlite:///{os.path.join(self.CURRENT_PATH, self.db_dir, self.db_name)}'

config = Config()
