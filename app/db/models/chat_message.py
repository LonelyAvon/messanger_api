import uuid
from datetime import date, datetime
from typing import List, Optional

from sqlalchemy import (
    ARRAY,
    SMALLINT,
    UUID,
    Boolean,
    Computed,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ChatMessage(Base):
    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    chat_id: Mapped[UUID] = mapped_column(
        ForeignKey("chats.id"), nullable=False, default=None
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"), nullable=False, default=None
    )
    message: Mapped[str] = mapped_column(String(2048), default=None)
    file: Mapped[Optional[str]] = mapped_column(String(255), default=None)

    user: Mapped["User"] = relationship(back_populates="user_chat_messages")  # type: ignore  # noqa: F821
    chat: Mapped["Chat"] = relationship(back_populates="user_chat_messages")  # type: ignore  # noqa: F821
