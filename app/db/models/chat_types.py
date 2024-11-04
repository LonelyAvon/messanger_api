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


class ChatType(Base):
    __tablename__ = "chat_types"
    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), unique=True, default=None)

    chats: Mapped[List["Chat"]] = relationship(back_populates="type", default=None) # type: ignore