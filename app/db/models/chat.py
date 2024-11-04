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
    type: Mapped[str] = mapped_column(String(255), default='person')
    name: Mapped[str] = mapped_column(String(255), default=None)

    user_chat: Mapped["UserChat"] = relationship(back_populates="chat", default=None) # type: ignore