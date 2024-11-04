from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, declared_attr
from datetime import date, datetime, timezone
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

class DateTimeMixin(MappedAsDataclass):
    """Класс данных для mixin даты и времени"""

    created_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        server_default=func.now(), 
        comment='Время создания'
    )
    updated_time: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=False),
        onupdate=func.now(),
        sort_order=999,
        comment='Время обновления'
    )


class MappedBase(DeclarativeBase):
   

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class DataClassBase(MappedAsDataclass, MappedBase):

    __abstract__ = True


class Base(MappedBase, DateTimeMixin):

    __abstract__ = True


