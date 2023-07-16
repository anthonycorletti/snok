from datetime import datetime
from typing import Optional
from uuid import uuid4

from pydantic import UUID4, BaseModel
from sqlalchemy import Column, DateTime
from sqlmodel import Field


class TimestampsMixin(BaseModel):
    created_at: Optional[datetime] = Field(
        sa_column=Column(
            DateTime,
            default=datetime.utcnow,
            nullable=False,
        )
    )
    updated_at: Optional[datetime] = Field(
        sa_column=Column(
            DateTime,
            default=datetime.utcnow,
            onupdate=datetime.utcnow,
            nullable=False,
        )
    )


class UUIDMixin(BaseModel):
    id: UUID4 = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
