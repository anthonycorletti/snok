from fastapi import FastAPI
from modal import Image, Secret, Stub, asgi_app

from {{ __template_name }}.config import Settings

stub = Stub(name="{{ __template_name }}")
Settings.Config.env_file = ".env.prod"
stub["env"] = Secret.from_dict(
    {str(k): str(v) for k, v in Settings().dict().items()}
)  # type: ignore
image = Image.debian_slim().pip_install_from_pyproject("pyproject.toml")


@stub.function(
    image=image,
    secret=stub["env"],
)
@asgi_app()
def _app() -> FastAPI:
    from {{ __template_name }}.app import app

    return app
