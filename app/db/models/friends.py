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
from app.db.models.chat_message import ChatMessage
from app.db.models.user_chat import UserChat


class FriendRequests(Base):
    __tablename__ = "friend_requests"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False, default=None)
    friend_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False, default=None)

    sender: Mapped["User"] = relationship(
        foreign_keys=[user_id],
        back_populates="sent_requests"
    )
    
    receiver: Mapped["User"] = relationship(
        foreign_keys=[friend_id],
        back_populates="received_requests"
    )

class Friends(Base):
    __tablename__ = "friends"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False, default=None)
    friend_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False, default=None)

    adder: Mapped["User"] = relationship(
        foreign_keys=[user_id],
        back_populates="friends_added"
    )
    
    added_friend: Mapped["User"] = relationship(
        foreign_keys=[friend_id],
        back_populates="friends_of"
    )