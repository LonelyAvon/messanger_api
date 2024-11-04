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
from sqlalchemy.dialects.postgresql import BYTEA
import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Chat(Base):
    __tablename__ = "chats"
    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    type_id: Mapped[UUID] = mapped_column(UUID, default=None)

    type: Mapped["ChatType"] = relationship(back_populates="chats", default=None) # type: ignore