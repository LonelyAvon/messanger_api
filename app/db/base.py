from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase
from app.db.metadata import meta
from datetime import date, datetime
from typing import List, Optional
import uuid
from sqlalchemy import (
    Computed,
    Date,
    DateTime,
    Float,
    Integer,
    String,
    text,
    UniqueConstraint,
    func,
    UUID,
    ForeignKey,
    SMALLINT,
    Boolean,
    ARRAY,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
class SqlalchemyBase(DeclarativeBase):
    """Base for all models."""

    metadata = meta


class Base(SqlalchemyBase):
    """Base for all models."""

    __abstract__ = True

    created_at = mapped_column(DateTime(timezone=False), nullable=False, server_default=func.now())
    updated_at = mapped_column(
        DateTime(timezone=False), nullable=False, server_default=func.now(), onupdate=func.now()
    )