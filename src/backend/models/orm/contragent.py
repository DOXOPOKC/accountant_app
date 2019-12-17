from sqlalchemy import Column, String, Date

from models.orm.base_model import Base


class Contragent(Base):
    name = Column(String, index=True)
    inn = Column(String)
    ur_adress = Column(String)
    fuct_adress = Column(String)
    ogrn = Column(String)
    date = Column(Date)
    klass = Column(String)
