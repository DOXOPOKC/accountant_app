from pydantic import BaseModel


class ContragentBase(BaseModel):
    name: str
    inn: str
    fuct_adress: str
    klass: str

    class Config:
        orm_mode = True


class ContragentGet(ContragentBase):
    ur_adress: str = None
    ogrn: str = None
    date: str = None


class ContragentCreate(ContragentBase):
    pass


class ContragentUpdate(ContragentGet):
    pass


class ContragentInDB(ContragentGet):
    id: int
