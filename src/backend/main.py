from fastapi import FastAPI
from starlette.requests import Request

from routes.api_router import router

from db.base import Session


app = FastAPI()

app.include_router(router)


@app.middleware('http')
def db_session_middleware(request: Request, call_next):
    request.state.db = Session()
    response = call_next(request)
    request.state.db.close()
    return response
