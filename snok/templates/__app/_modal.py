import modal
from fastapi import FastAPI

from {{ __template_name }}.config import settings
from {{ __template_name }}.app import app
from {{ __template_name }}.const import BASE_APP_PACKAGES

stub = modal.Stub(
    name={{ __template_name }},
)

stub["env"] = modal.Secret(settings.dict())

image = modal.Image.debian_slim().pip_install(BASE_APP_PACKAGES)


@stub.asgi(image=image, secret=stub["env"],)
def _app() -> FastAPI:
    return app


if __name__ == "__main__":
    stub.serve()
