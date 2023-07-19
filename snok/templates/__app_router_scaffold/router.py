from fastapi import APIRouter, Response, status
from typing import List

from {{ __template_name }}.kit.routers import _APIRoute

router = APIRouter(
    route_class=_APIRoute,
    tags=["{{ __template_plural_namespace }}"],
)

@router.post("/{{ __template_plural_namespace }}", response_model={{__template_plural_namespace_caps}}Read)
async def _create_{{ __template_plural_namespace }}() -> {{__template_plural_namespace_caps}}Read:
    return None


@router.get("/{{ __template_plural_namespace }}", response_model=List[{{__template_plural_namespace_caps}}Read])
async def _list_{{ __template_plural_namespace }}() -> List[{{__template_plural_namespace_caps}}Read]:
    return None


@router.get("/{{ __template_plural_namespace }}/{id}", response_model={{__template_plural_namespace_caps}}Read)
async def _get_{{ __template_plural_namespace }}() -> {{__template_plural_namespace_caps}}Read:
    return None


@router.put("/{{ __template_plural_namespace }}/{id}", response_model={{__template_plural_namespace_caps}}Read)
async def _update_{{ __template_plural_namespace }}() -> {{__template_plural_namespace_caps}}Read:
    return None


@router.delete("/{{ __template_plural_namespace }}/{id}", response_model=Response)
async def _delete_{{ __template_plural_namespace }}() -> Response:
    return Response(status_code=status.HTTP_204_NO_CONTENT)
