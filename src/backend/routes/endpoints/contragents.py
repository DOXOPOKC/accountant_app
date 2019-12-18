from typing import List

from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from models.orm.contragent import Contragent
from models.data.contragent import ContragentGet, ContragentBase
from utils.db import get_db
# from utils.parsers.contragents_xlsx import #TODO

router = APIRouter()


@router.get('/contragents', response_model=List[ContragentGet])
def get_contragents(db: Session = Depends(get_db)):
    return db.query(Contragent).all()


@router.post('/contragents')
def upload_contragents(db: Session = Depends(get_db),
                       xlsx_file: UploadFile = File()):
    
