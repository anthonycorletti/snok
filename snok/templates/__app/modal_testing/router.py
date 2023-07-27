import time

from fastapi import APIRouter

from {{ __template_name }}._modal import Cache, Queue, Worker
from {{ __template_name }}.kit.routers import _APIRoute
from {{ __template_name }}.logger import log

router = APIRouter(
    route_class=_APIRoute,
    tags=["modal_testing"],
)

#
#   NOTE: This module can be safely deleted. It's only purpose is to demo
#   modal functionality. You can repurpose these functions for your own apps.
#


@router.get("/cache", response_model=None)
async def _test_cache() -> None:
    get = await Cache.get("test")
    log.info(f"get: {get}")
    contains = await Cache.contains("test")
    log.info(f"contains: {contains}")
    await Cache.put("test", "test")
    await Cache.put("test", "toast")
    get = await Cache.get("test")
    log.info(f"get: {get}")
    contains = await Cache.contains("test")
    log.info(f"contains: {contains}")
    await Cache.pop("test")
    get = await Cache.get("test")
    log.info(f"get: {get}")
    contains = await Cache.contains("test")
    log.info(f"contains: {contains}")
    log.info("popping again...")
    await Cache.pop("test")


@router.get("/queue", response_model=None)
async def _test_queue() -> None:
    get = await Queue.get()  # type: ignore
    log.info(f"get: {get}")
    await Queue.put("test")  # type: ignore
    get = await Queue.get()  # type: ignore
    log.info(f"get: {get}")
    await Queue.put_many(["test", "toast"])  # type: ignore
    get = await Queue.get_many(2)  # type: ignore
    log.info(f"get: {get}")
    await Queue.put_many(["test", "toast"])  # type: ignore
    get = await Queue.get_many(3)  # type: ignore
    log.info(f"get: {get}")


@router.get("/worker", response_model=None)
async def _test_worker(backgrounded: bool = False) -> None:
    async def thing_doer() -> None:
        log.info("doing things")
        time.sleep(30)
        log.info("done doing things")
        return

    log.info("running things")
    await Worker.run(
        stub_name="{{ __template_name }}",
        func_name="_run",
        backgrounded=backgrounded,
        func=thing_doer,
    )
    log.info("done running things")

    # NOTE: this is a test of the worker running a function that is not
    #       defined in the stub, when a function is not found in the stub
    #       modal will raise an exception
    # log.info("running things")
    # await Worker.run(
    #     stub_name="{{ __template_name }}",
    #     func_name="_run_worker",
    #     backgrounded=backgrounded,
    #     func=thing_doer,
    # )
    # log.info("done running things")
