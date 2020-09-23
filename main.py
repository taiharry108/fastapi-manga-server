from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.logger import logger
from fastapi.templating import Jinja2Templates
from routers import main, google_auth, user
from core.singleton_aiohttp import SingletonAiohttp
from database import models
from database.database import engine


models.Base.metadata.create_all(bind=engine)


fastAPI_logger = logger  # convenient name

origins = ["http://localhost:4200"]


async def on_start_up():
    fastAPI_logger.info("on_start_up")
    # d = Downloader(SingletonAiohttp.get_session())


async def on_shutdown():
    fastAPI_logger.info("on_shutdown")
    await SingletonAiohttp.close_aiohttp_client()

app = FastAPI(on_startup=[on_start_up], on_shutdown=[on_shutdown])
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):    
    return templates.TemplateResponse("index.html", {"request": request})

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
