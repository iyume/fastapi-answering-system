from typing import Optional


class UserPayload():
    def __init__(self, user_dict: Optional[dict] = None) -> None:
        self.user_dict = user_dict
        if isinstance(user_dict, dict):
            self.id: str = user_dict.get('id', None)
            self.name: str = user_dict.get('iss', None)
            self.email: str = user_dict.get('email', None)
            self.exp: int = user_dict.get('exp', 1000000000)
            self.is_active: bool = user_dict.get('is_active', True)
            self.is_superuser: bool = user_dict.get('is_superuser', False)

    @property
    def is_authenticated(self) -> bool:
        if not self.user_dict:
            return False
        return self.is_active


class UserDetail():
    ...

