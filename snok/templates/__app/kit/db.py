from datetime import datetime
from typing import Optional
from uuid import uuid4

from pydantic import UUID4, BaseModel
from sqlalchemy import Column, DateTime
from sqlmodel import Field, MetaData, SQLModel

_metadata = MetaData()
_metadata.naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)" "s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


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
    deleted_at: Optional[datetime] = Field(
        sa_column=Column(
            DateTime,
            nullable=True,
        )
    )


class UUIDMixin(BaseModel):
    id: UUID4 = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )



class Model(SQLModel):
    __abstract__ = True

    metadata = _metadata


class TimestampedModel(Model, TimestampsMixin):
    __abstract__ = True


class RecordModel(TimestampedModel, UUIDMixin):
    __abstract__ = True
