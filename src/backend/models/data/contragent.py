from pydantic import BaseModel


class ContragentBase(BaseModel):
    name: str
    inn: str
    ur_adress: str
    klass: str

    class Config:
        orm_mode = True


class ContragentGet(ContragentBase):
    fuct_adress: str = None
    ogrn: str = None
    date: str = None


class ContragentCreate(ContragentBase):
    pass


class ContragentUpdate(ContragentGet):
    pass


class ContragentInDB(ContragentGet):
    id: int
