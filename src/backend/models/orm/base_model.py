from sqlalchemy import Column
from sqlalchemy.types import BigInteger
from sqlalchemy.ext.declarative import declarative_base, declared_attr


class CustomBase(object):
    __abstract__ = True

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


Base = declarative_base(cls=CustomBase)
