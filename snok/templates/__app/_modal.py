from typing import Any, Callable, List, Optional

from {{ __template_name }}.config import Settings
from {{ __template_name }}.logger import log
from fastapi import FastAPI
from modal import Dict, Function, Image, Secret, Stub, asgi_app
from modal import Queue as ModalQueue

stub = Stub(name="{{ __template_name }}")
Settings.Config.env_file = ".env.prod"
stub["env"] = Secret.from_dict(
    {str(k): str(v) for k, v in Settings().dict().items()}  # type: ignore
)

_kv = Dict.new()
stub._kv = _kv
stub._kv.persisted(label="{{ __template_name }}_kv")

_queue = ModalQueue.new()
stub._queue = _queue
stub._queue.persisted(label="{{ __template_name }}_queue")

image = Image.debian_slim().pip_install_from_pyproject("pyproject.toml")


@stub.function(
    image=image,
    secret=stub["env"],
)
@asgi_app(
    label="{{ __template_name }}",
)
def _app() -> FastAPI:
    from {{ __template_name }}.app import app

    return app


class Cache:
    @staticmethod
    async def get(key: str) -> Any:
        try:
            return await stub.app._kv.get.aio(key)
        except KeyError as e:
            log.error(f"Cache.get: key ({key}) not found")
            return None

    @staticmethod
    async def contains(key: str) -> Any:
        return await stub.app._kv.contains.aio(key)

    @staticmethod
    async def put(key: str, value: Any) -> None:
        return await stub.app._kv.put.aio(key, value)

    @staticmethod
    async def pop(key: str) -> None:
        try:
            return await stub.app._kv.pop.aio(key)
        except KeyError as e:
            log.error(f"Cache.pop: key ({key}) not found")
            return None


class Queue:
    @staticmethod
    async def get(block: bool = False, timeout: Optional[float] = None) -> Any:
        return await stub.app._queue.get.aio(block=block, timeout=timeout)

    @staticmethod
    async def get_many(
        n: int, block: bool = False, timeout: Optional[float] = None
    ) -> List[Any]:
        return await stub.app._queue.get_many.aio(
            n_values=n, block=block, timeout=timeout
        )

    @staticmethod
    async def put(value: Any) -> None:
        return await stub.app._queue.put.aio(v=value)

    @staticmethod
    async def put_many(values: List[Any]) -> None:
        return await stub.app._queue.put_many.aio(vs=values)


class Worker:
    @staticmethod
    async def run(
        stub_name: str,
        func_name: str,
        backgrounded: bool = True,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        worker = await Function.lookup.aio(stub_name, func_name)
        if backgrounded:
            await worker.spawn.aio(*args, **kwargs)
        else:
            await worker.call.aio(*args, **kwargs)


@stub.function(
    image=image,
    secret=stub["env"],
)
async def _run(func: Callable, *args: Any, **kwargs: Any) -> None:
    await func(*args, **kwargs)
