import os

from httpx import AsyncClient

from {{ __template_name }} import __version__
from {{ __template_name }}.config import settings


async def test_tz() -> None:
    assert os.environ["TZ"] == "UTC"


async def test_livez(client: AsyncClient) -> None:
    response = await client.get("/livez")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert response.json()["message"] == "ok"
    assert "version" not in response.json()


async def test_readyz(client: AsyncClient) -> None:
    response = await client.get("/readyz")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert response.json()["message"] == "ok"
    assert response.json()["version"] == __version__


async def test_settings() -> None:
    assert settings.ENV == "test"
