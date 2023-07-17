from fastapi import APIRouter

from {{ __template_name }}.kit.routers import _APIRoute

router = APIRouter(
    route_class=_APIRoute,
    tags=["{{ __template_router_name }}"],
)

{% for route in __template_router_routes %}
@router.get("/{{ route }}", response_model=None)
async def _{{ route }}() -> None:
    return None
{% endfor %}
