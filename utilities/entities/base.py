from pydantic import BaseModel, Extra, conint

BASE_MODEL = BaseModel
Extra = Extra


def create_conint(*args, **kwargs):
    return conint(*args, **kwargs)


class EntityBase(BASE_MODEL):
    __tablename__ = "entity_base"

    class Config:
        extra = Extra.forbid
