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
from app.db.models.chat_message import ChatMessage


class Chat(Base):
    __tablename__ = "chats"
    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    type: Mapped[str] = mapped_column(
        String(255), default="personal", server_default="personal"
    )
    name: Mapped[str] = mapped_column(String(255), default=None)

    user_chat: Mapped["UserChat"] = relationship(back_populates="chat")  # type: ignore  # noqa: F821
    user_chat_messages: Mapped[List["ChatMessage"]] = relationship(
        back_populates="chat"
    )  # noqa: F821
