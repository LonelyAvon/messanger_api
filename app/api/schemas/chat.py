from datetime import datetime, timezone
from typing import Literal, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_validator

from app.api.schemas.user import ChatUser

from .user import Photo


class ChatCreate(BaseModel):
    users: list[UUID]
    name: Optional[str] = None
    type: Literal["personal", "group"]


class ChatRead(BaseModel):
    id: UUID
    name: str
    type: Literal["personal", "group"]

    class Config:
        from_attributes = True


class RedisChatMessage(BaseModel):
    surname: str
    name: str
    patronymic: str
    message: str
    created_at: datetime = datetime.now(timezone.utc)


class ChatMessage(BaseModel):
    message: Optional[str]
    created_time: Optional[datetime]


class ChatPreview(Photo):
    id: UUID
    chat_name: str
    type: Literal["personal", "group"]
    last_message: Optional[ChatMessage] = None


class ChatMessageWithPhoto(Photo):
    sender_id: UUID
    message: Optional[str]
    created_time: Optional[datetime]
    surname: str
    name: str
    patronymic: Optional[str] = None


class ChatInfo(BaseModel):
    id: UUID
    chat_name: str
    photo: Optional[str]
    messages: Optional[list[ChatMessageWithPhoto]]


class ChatMessageUserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    message: str
    file: Optional[str] = None
    created_time: str
    user: ChatUser

    @field_validator("created_time", mode="before")
    def validate_created_time(cls, value):
        # 17.05 10:04
        return datetime.strftime(value, "%m.%d %H:%M")
