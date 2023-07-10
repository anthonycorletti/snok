import os
import time
from typing import Callable

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from {{ __template_name }} import __version__
from {{ __template_name }}.const import LOCAL_DOMAINS, ORIGINS, EXTRA_ORIGINS
from {{ __template_name }}.exc import exception_handlers
from {{ __template_name }}.log import log
from {{ __template_name }}.settings import settings
from {{ __template_name }}.routers import health
from {{ __template_name }}.views import home

app = FastAPI(
    name="{{ __template_name }}",
    version=__version__,
    exception_handlers=exception_handlers,
)

os.environ["TZ"] = "UTC"

if any(domain in settings.APP_URL for domain in LOCAL_DOMAINS):
    ORIGINS.extend(EXTRA_ORIGINS)


app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.API_SECRET_KEY,
)
app.mount(
    name="static",
    path="/static",
    app=StaticFiles(directory="static"),
)


@app.on_event("startup")
async def startup() -> None:
    log.debug({"message": "starting up"})


@app.middleware("http")
async def add_process_time_header(request: Request, call_next: Callable) -> Response:
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time-Seconds"] = str(process_time)
    return response


app.include_router(health.router)
app.include_router(home.router)
