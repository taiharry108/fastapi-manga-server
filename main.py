from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import manhuaren
from core.downloader import Downloader
from fastapi.logger import logger
from core.singleton_aiohttp import SingletonAiohttp


fastAPI_logger = logger  # convenient name

origins = ["http://localhost:4200"]


async def on_start_up():
    fastAPI_logger.info("on_start_up")
    d = Downloader(SingletonAiohttp.get_session())


async def on_shutdown():
    fastAPI_logger.info("on_shutdown")
    await SingletonAiohttp.close_aiohttp_client()

app = FastAPI(on_startup=[on_start_up], on_shutdown=[on_shutdown])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    manhuaren.router,
    prefix="/api/manhuaren",
    tags=["manhuaren"],
    responses={404: {"description": "Not Found"}}
)
