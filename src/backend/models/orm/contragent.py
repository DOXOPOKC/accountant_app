from enum import Enum

from sqlalchemy import Column, String
from sqlalchemy.types import BigInteger, Date
from sqlalchemy.dialects.postgresql import ENUM

from models.orm.base_model import Base


class KlassType(Enum):
    ur = 'Юридическое лицо'
    fl = 'Физическое лицо'


class Contragent(Base):
    name = Column(String(), index=True)
    inn = Column(BigInteger())
    fuct_adress = Column(String())
    klass = Column(ENUM(KlassType, name='klass_enum'),
                   nullable=False, default=KlassType.ur)
    ur_adress = Column(String())
    ogrn = Column(BigInteger(), nullable=True)
    reg_date = Column(Date(), nullable=True)
