from fastapi import APIRouter

from {{ __template_name }}.home.views import router as home_router
from {{ __template_name }}.kit.routers import _APIRoute

router = APIRouter(
    route_class=_APIRoute,
)

router.include_router(router=home_router)
