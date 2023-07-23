from typing import Any, List, Optional

from pydantic import UUID4
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from {{ __template_name }}.models.{{ __template_plural_namespace }} import {{ __template_plural_namespace_caps }}
from {{ __template_name }}.{{ __template_plural_namespace }}.schemas import {{ __template_plural_namespace_caps }}Create, {{ __template_plural_namespace_caps }}QueryParams, {{ __template_plural_namespace_caps }}Update


class {{ __template_plural_namespace_caps }}Service:
    async def create(self, db: AsyncSession, {{ __template_plural_namespace }}_create: {{ __template_plural_namespace_caps }}Create) -> {{ __template_plural_namespace_caps }}:
        db_{{ __template_plural_namespace }} = {{ __template_plural_namespace_caps }}(**{{ __template_plural_namespace }}_create.dict())
        db.add(db_{{ __template_plural_namespace }})
        await db.commit()
        await db.refresh(db_{{ __template_plural_namespace }})
        return db_{{ __template_plural_namespace }}

    async def get(self, db: AsyncSession, _id: UUID4) -> Optional[{{ __template_plural_namespace_caps }}]:
        results = await db.execute(select({{ __template_plural_namespace_caps }}).where({{ __template_plural_namespace_caps }}.id == _id))
        return results.scalars().first()

    async def list(
        self,
        db: AsyncSession,
        params: {{ __template_plural_namespace_caps }}QueryParams,
        order_by: str = "updated_at",
        order_direction: str = "desc",
        offset: int = 0,
        limit: int = 10,
    ) -> List[{{ __template_plural_namespace_caps }}]:
        results = await db.execute(
            select({{ __template_plural_namespace_caps }})
            .filter_by(**params.dict(exclude_none=True))
            .order_by(getattr(getattr({{ __template_plural_namespace_caps }}, order_by), order_direction)())
            .offset(offset)
            .limit(limit)
        )
        return results.scalars().all()

    async def update(
        self, db: AsyncSession, {{ __template_namespace }}: {{ __template_plural_namespace_caps }}, {{ __template_plural_namespace }}_update: {{ __template_plural_namespace_caps }}Update
    ) -> {{ __template_plural_namespace_caps }}:
        update_data = {{ __template_plural_namespace }}_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr({{ __template_namespace }}, key, value)
        db.add({{ __template_namespace }})
        await db.commit()
        await db.refresh({{ __template_namespace }})
        return {{ __template_namespace }}

    async def delete(self, db: AsyncSession, {{ __template_namespace }}: {{ __template_plural_namespace_caps }}) -> None:
        await db.delete({{ __template_namespace }})
        await db.commit()
        return None
