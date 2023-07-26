import os
import time
from typing import Callable

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from {{ __template_name }} import __version__
from {{ __template_name }}.const import LOCAL_DOMAINS, ORIGINS, EXTRA_ORIGINS
from {{ __template_name }}.exceptions import exception_handlers
from {{ __template_name }}.logger import log
from {{ __template_name }}.config import settings
from {{ __template_name }}.health.router import router as health_router
from {{ __template_name }}.router import router

os.environ["TZ"] = "UTC"


def configure_cors(app: FastAPI) -> None:
    if any(domain in settings.APP_URL for domain in LOCAL_DOMAINS):
        ORIGINS.extend(EXTRA_ORIGINS)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def add_session_middleware(app: FastAPI) -> None:
    app.add_middleware(
        SessionMiddleware,
        secret_key=settings.API_SECRET_KEY,
    )

# TODO: frontend with htmx and tailwind
# def mount_directories(app: FastAPI) -> None:
#     app.mount(
#         name="static",
#         path="/static",
#         app=StaticFiles(directory="static"),
#     )

def add_http_middleware(app: FastAPI) -> None:
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next: Callable,) -> Response:
        start_time = time.time() * 1000
        response = await call_next(request)
        request_time_ms = int(time.time() * 1000 - start_time)
        response.headers["x-request-time-ms"] = str(request_time_ms)
        return response


def configure_events(app: FastAPI) -> None:
    @app.on_event("startup")
    async def startup() -> None:
        log.debug({"message": "starting up"})

    @app.on_event("shutdown")
    async def shutdown() -> None:
        log.debug({"message": "shutting down"})


def generate_unique_openapi_id(route: APIRoute) -> str:
    return f"{route.tags[0]}:{route.name}"


def create_app() -> FastAPI:
    app = FastAPI(
        title="{{ __template_name }}",
        version=__version__,
        exception_handlers=exception_handlers,
        generate_unique_id_function=generate_unique_openapi_id
    )

    # TODO: frontend with htmx and tailwind
    # mount_directories(app)
    configure_events(app)
    configure_cors(app)
    add_http_middleware(app)
    add_session_middleware(app)

    app.include_router(health_router)
    app.include_router(router)

    return app


app = create_app()
