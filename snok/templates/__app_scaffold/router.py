from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, Response, status
from pydantic import UUID4
from sqlmodel.ext.asyncio.session import AsyncSession

from {{ __template_name }}.database import db_session
from {{ __template_name }}.kit.routers import _APIRoute
from {{ __template_name }}.models.{{ __template_plural_namespace }} import {{ __template_plural_namespace_caps }}
from {{ __template_name }}.{{ __template_plural_namespace }}.schemas import {{ __template_plural_namespace_caps }}Create, {{ __template_plural_namespace_caps }}QueryParams, {{ __template_plural_namespace_caps }}Update
from {{ __template_name }}.{{ __template_plural_namespace }}.service import {{ __template_plural_namespace_caps }}Service

router = APIRouter(
    route_class=_APIRoute,
    tags=["{{ __template_plural_namespace }}"],
)


@router.get("/{{ __template_plural_namespace }}", response_model=List[{{ __template_plural_namespace_caps }}])
async def _list_{{ __template_plural_namespace }}(
    params: {{ __template_plural_namespace_caps }}QueryParams = Depends(),
    order_by: str = "updated_at",
    order_direction: str = "desc",
    offset: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(db_session),
    {{ __template_plural_namespace }}_service: {{ __template_plural_namespace_caps }}Service = Depends({{ __template_plural_namespace_caps }}Service),
) -> List[{{ __template_plural_namespace_caps }}]:
    return await {{ __template_plural_namespace }}_service.list(
        params=params,
        db=db,
        order_by=order_by,
        order_direction=order_direction,
        offset=offset,
        limit=limit,
    )


@router.post("/{{ __template_plural_namespace }}", response_model={{ __template_plural_namespace_caps }})
async def _create_{{ __template_plural_namespace }}(
    {{ __template_plural_namespace }}_create: {{ __template_plural_namespace_caps }}Create = Body(...),
    db: AsyncSession = Depends(db_session),
    {{ __template_plural_namespace }}_service: {{ __template_plural_namespace_caps }}Service = Depends({{ __template_plural_namespace_caps }}Service),
) -> {{ __template_plural_namespace_caps }}:
    return await {{ __template_plural_namespace }}_service.create(db=db, {{ __template_plural_namespace }}_create={{ __template_plural_namespace }}_create)


@router.get("/{{ __template_plural_namespace }}/{_id}", response_model={{ __template_plural_namespace_caps }})
async def _get_{{ __template_plural_namespace }}(
    _id: UUID4,
    db: AsyncSession = Depends(db_session),
    {{ __template_plural_namespace }}_service: {{ __template_plural_namespace_caps }}Service = Depends({{ __template_plural_namespace_caps }}Service),
) -> {{ __template_plural_namespace_caps }}:
    {{ __template_namespace }} = await {{ __template_plural_namespace }}_service.get(db=db, _id=_id)
    if not {{ __template_namespace }}:
        raise HTTPException(status_code=404, detail="Not found")
    return {{ __template_namespace }}


@router.put("/{{ __template_plural_namespace }}/{_id}", response_model={{ __template_plural_namespace_caps }})
async def _update_{{ __template_plural_namespace }}(
    _id: UUID4,
    {{ __template_plural_namespace }}_update: {{ __template_plural_namespace_caps }}Update = Body(...),
    db: AsyncSession = Depends(db_session),
    {{ __template_plural_namespace }}_service: {{ __template_plural_namespace_caps }}Service = Depends({{ __template_plural_namespace_caps }}Service),
) -> {{ __template_plural_namespace_caps }}:
    {{ __template_namespace }} = await {{ __template_plural_namespace }}_service.get(db=db, _id=_id)
    if not {{ __template_namespace }}:
        raise HTTPException(status_code=404, detail="Not found")
    return await {{ __template_plural_namespace }}_service.update(
        db=db, {{ __template_namespace }}={{ __template_namespace }}, {{ __template_plural_namespace }}_update={{ __template_plural_namespace }}_update
    )


@router.delete("/{{ __template_plural_namespace }}/{_id}", response_class=Response)
async def _delete_{{ __template_plural_namespace }}(
    _id: UUID4,
    db: AsyncSession = Depends(db_session),
    {{ __template_plural_namespace }}_service: {{ __template_plural_namespace_caps }}Service = Depends({{ __template_plural_namespace_caps }}Service),
) -> Response:
    {{ __template_namespace }} = await {{ __template_plural_namespace }}_service.get(db=db, _id=_id)
    if not {{ __template_namespace }}:
        raise HTTPException(status_code=404, detail="Not found")
    await {{ __template_plural_namespace }}_service.delete(db=db, {{ __template_namespace }}={{ __template_namespace }})
    return Response(status_code=status.HTTP_204_NO_CONTENT)
