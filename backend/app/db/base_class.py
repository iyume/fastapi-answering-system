from typing import Any

from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    id: Any
    __name__: str
    # Generate __tablename__ automatically
    def __init__(self, **kwargs: Any):
        cls_ = type(self)
        for k in kwargs:
            if not hasattr(cls_, k):
                raise AttributeError(
                    f"{k} is an invalid keyword argument for {cls_.__name__}")
            setattr(self, k, kwargs[k])
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
