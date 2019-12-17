from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models.orm.contragent import Contragent
from models.data.contragent import ContragentGet, ContragentBase
from utils.db import get_db

router = APIRouter()


@router.get('/', response_model=List[ContragentGet])
def get_contragents(db: Session = Depends(get_db)):
    return db.query(Contragent).all()
