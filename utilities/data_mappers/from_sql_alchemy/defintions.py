from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase

DeclarativeBase = DeclarativeBase(metadata=MetaData())
String = String
DateTime = DateTime
Integer = Integer
ForeignKey = ForeignKey


def Column_(*args, **kwargs):
    return Column(*args, **kwargs)


def relationship_(*args, **kwargs):
    return relationship(*args, **kwargs)
