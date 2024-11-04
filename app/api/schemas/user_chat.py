from datetime import datetime
from pydantic import BaseModel
from uuid import UUID

class UserChatRead(BaseModel):
    id: UUID
    chat_id: UUID
    user_id: UUID

class UserChatCreate(BaseModel):
    chat_id: UUID
    user_id: UUID

class UserChatSchema(BaseModel):
    id: UUID
    chat_id: UUID
    user_id: UUID
    updated_at: datetime
    created_at: datetime