from datetime import datetime

from fastapi import APIRouter

from {{ __template_name }} import __version__
from {{ __template_name }}._types import HealthResponse
from {{ __template_name }}.utils.routers import _APIRoute

router = APIRouter(
    route_class=_APIRoute,
    tags=["health"],
)


@router.get("/healthcheck", response_model=HealthResponse)
async def healthcheck() -> HealthResponse:
    return HealthResponse(
        message="ok",
        version=__version__,
        time=datetime.utcnow(),
    )
