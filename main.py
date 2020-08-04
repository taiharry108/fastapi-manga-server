from typing import Optional

from fastapi import FastAPI, Header
from routers import manhuaren

app = FastAPI()

app.include_router(
    manhuaren.router,
    prefix="/api/manhuaren",
    tags=["manhuaren"],
    responses={404: {"description": "Not Found"}}
)