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
from app.db.models.friends import FriendRequests, Friends


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String(255), unique=True, default=None)
    password: Mapped[BYTEA] = mapped_column(type_=BYTEA(1024), default=None)
    surname: Mapped[str] = mapped_column(String(255), default=None)
    name: Mapped[str] = mapped_column(String(255), default=None)
    patronymic: Mapped[Optional[str]] = mapped_column(String(255), default=None)

    email: Mapped[str] = mapped_column(String(255), unique=True, default=None, nullable=True)
    is_verified_email: Mapped[bool] = mapped_column(Boolean, server_default='false', default=None)

    role: Mapped[str] = mapped_column(String(50), server_default="user", default=None)
    is_archived: Mapped[bool] = mapped_column(Boolean, server_default='false', default=None)
    last_visit: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), default=None)
    photo: Mapped[Optional[str]] = mapped_column(String(255), default=None)

    user_chats: Mapped[List[UserChat]] = relationship(back_populates="user") 
    user_chat_messages: Mapped[List[ChatMessage]] = relationship(back_populates="user")

    sent_requests: Mapped[List[FriendRequests]] = relationship(
        foreign_keys="FriendRequests.user_id",
        back_populates="sender"
    )
    
    received_requests: Mapped[List[FriendRequests]] = relationship(
        foreign_keys="FriendRequests.friend_id",
        back_populates="receiver"
    )

    # Отношения для Friends
    friends_added: Mapped[List[Friends]] = relationship(
        foreign_keys="Friends.user_id",
        back_populates="adder"
    )
    
    friends_of: Mapped[List[Friends]] = relationship(
        foreign_keys="Friends.friend_id",
        back_populates="added_friend"
    )



