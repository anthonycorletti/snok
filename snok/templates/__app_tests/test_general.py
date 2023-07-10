import os

from httpx import AsyncClient

from {{ __template_name }} import __version__, gunicorn_conf
from {{ __template_name }}.settings import settings


async def test_tz() -> None:
    assert os.environ["TZ"] == "UTC"


async def test_healthcheck(client: AsyncClient) -> None:
    response = await client.get("/healthcheck")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert response.json()["message"] == "ok"
    assert response.json()["version"] == __version__


async def test_gunicorn_settings() -> None:
    assert gunicorn_conf.worker_class == "uvicorn.workers.UvicornWorker"
    assert gunicorn_conf.port == 8000
    assert gunicorn_conf.bind == ":8000"
    assert gunicorn_conf.workers == 1


async def test_settings() -> None:
    assert settings.ENV == "test"
