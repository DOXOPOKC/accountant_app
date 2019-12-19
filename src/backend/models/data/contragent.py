from pydantic import BaseModel

from models.orm.contragent import KlassType
from datetime import date


class ContragentBase(BaseModel):
    name: str
    inn: int
    fuct_adress: str
    klass: KlassType

    class Config:
        orm_mode = True


class ContragentGet(ContragentBase):
    ur_adress: str = None
    ogrn: int = None
    reg_date: date = None


class ContragentCreate(ContragentBase):
    pass


class ContragentUpdate(ContragentGet):
    pass


class ContragentInDB(ContragentGet):
    id: int
