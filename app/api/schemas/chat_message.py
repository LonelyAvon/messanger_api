from uuid import UUID
from pydantic import BaseModel


class ChatMessageCreate(BaseModel):
    chat_id: str
    user_id: str
    message: str