from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.logger import logger
from routers import main, google_auth, user
from database import models
from database.database import engine


models.Base.metadata.create_all(bind=engine)


fastAPI_logger = logger  # convenient name

origins = ["http://localhost:4200", "http://localhost:8001"]


async def on_start_up():
    fastAPI_logger.info("on_start_up")


async def on_shutdown():
    fastAPI_logger.info("on_shutdown")    

app = FastAPI(on_startup=[on_start_up], on_shutdown=[on_shutdown])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    main.router,
    prefix="/api",
    responses={404: {"description": "Not Found"}}
)

app.include_router(
    google_auth.router,
    prefix="/api/auth",
    responses={404: {"description": "Not Found"}}
)

app.include_router(
    user.router,
    prefix="/api/user",
    responses={404: {"description": "Not Found"}}
)
