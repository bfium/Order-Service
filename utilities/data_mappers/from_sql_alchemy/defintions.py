from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, MetaData
from sqlalchemy.orm import relationship, declarative_base

DeclarativeBase = declarative_base()
String = String
DateTime = DateTime
Integer = Integer
ForeignKey = ForeignKey


def Column_(*args, **kwargs):
    return Column(*args, **kwargs)


def relationship_(*args, **kwargs):
    return relationship(*args, **kwargs)
