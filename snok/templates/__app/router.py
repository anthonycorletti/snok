from fastapi import APIRouter

from {{ __template_name }}.const import API_V0
from {{ __template_name }}.kit.routers import _APIRoute
from {{ __template_name }}.modal_testing.router import router as modal_testing_router

router = APIRouter(
    prefix=API_V0,
    route_class=_APIRoute,
)

router.include_router(modal_testing_router)
