from fastapi import APIRouter

from {{ __template_name }}.const import API_V0
from {{ __template_name }}.kit.routers import _APIRoute

router = APIRouter(
    prefix=API_V0,
    route_class=_APIRoute,
)
