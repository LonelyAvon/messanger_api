from datetime import datetime, timezone
from typing import Literal, Optional
from uuid import UUID
from pydantic import BaseModel

from app.api.schemas.user import ChatUser


class ChatCreate(BaseModel):
    users: list[UUID]
    name: str
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

class ChatPreview(BaseModel):
    id: UUID
    chat_name: str
    photo: Optional[str] = None
    type: Literal["personal", "group"]
    last_message: Optional[ChatMessage] = None

class ChatInfo(BaseModel):
    id: UUID
    chat_name: str
    photo: Optional[str]
    type: Literal["personal", "group"]
    messages: Optional[list[ChatMessage]]