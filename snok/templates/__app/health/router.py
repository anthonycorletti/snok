from datetime import datetime

from fastapi import APIRouter

from {{ __template_name }} import __version__
from {{ __template_name }}.health.schemas import LivezResponse, ReadyzResponse
from {{ __template_name }}.kit.routers import _APIRoute

router = APIRouter(
    route_class=_APIRoute,
    tags=["health"],
)


@router.get("/livez", response_model=LivezResponse)
async def _livez() -> LivezResponse:
    return LivezResponse(
        message="ok",
    )


@router.get("/readyz", response_model=ReadyzResponse)
async def _readyz() -> ReadyzResponse:
    return ReadyzResponse(
        message="ok",
        version=__version__,
        time=datetime.utcnow(),
    )
