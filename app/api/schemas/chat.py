from datetime import datetime, timezone
from typing import Literal, Optional
from uuid import UUID
from pydantic import BaseModel

from app.api.schemas.user import ChatUser


class ChatCreate(BaseModel):
    users: list[UUID]
    name: str
    type: Literal["person", "group"]

class ChatRead(BaseModel):
    id: UUID
    name: str
    type: Literal["person", "group"]


class ChatMessage(BaseModel):
    user: Optional[ChatUser] = None
    message: str
    created_at: datetime = datetime.now(timezone.utc)    