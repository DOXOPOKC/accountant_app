from fastapi import APIRouter


from .endpoints import contragents


router = APIRouter()

router.include_router(contragents.router, prefix="/api", tags=["contragents"])