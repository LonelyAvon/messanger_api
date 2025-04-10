import uuid

from sqlalchemy import (
    UUID,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class FriendRequests(Base):
    __tablename__ = "friend_requests"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"), nullable=False, default=None
    )
    friend_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"), nullable=False, default=None
    )

    sender: Mapped["User"] = relationship(  # noqa: F821
        foreign_keys=[user_id], back_populates="sent_requests"
    )

    receiver: Mapped["User"] = relationship(  # noqa: F821
        foreign_keys=[friend_id], back_populates="received_requests"
    )


class Friends(Base):
    __tablename__ = "friends"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"), nullable=False, default=None
    )
    friend_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"), nullable=False, default=None
    )

    adder: Mapped["User"] = relationship(  # noqa: F821
        foreign_keys=[user_id], back_populates="friends_added"
    )

    added_friend: Mapped["User"] = relationship(  # noqa: F821
        foreign_keys=[friend_id], back_populates="friends_of"
    )
