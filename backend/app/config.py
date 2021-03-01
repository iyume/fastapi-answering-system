import os
import secrets

try:
    import pretty_errors
except ImportError:
    ...
else:
    pretty_errors.replace_stderr()


class Config():
    __name__ = 'config'

    access_token_exp_hours = 24 * 8 # exp in eight days

    db_dir = 'db'
    db_name = 'all.db'

    secret_key = 'ND87artiLDGlsGpRdsLasyVR_XBIi7tkefnS_1aqhbo'

    @property
    def ACCESS_TOKEN_EXP_HOURS(self) -> int:
        return self.access_token_exp_hours

    @property
    def CURRENT_PATH(self) -> str:
        return os.path.dirname(os.path.realpath(__file__))

    @property
    def DATABASE_URI(self) -> str:
        return f'sqlite:///{os.path.join(self.CURRENT_PATH, self.db_dir, self.db_name)}'

    @property
    def SECRET_KEY(self) -> str:
        return self.secret_key


config = Config()
