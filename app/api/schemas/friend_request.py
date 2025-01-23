from typing import Optional
from uuid import UUID
from pydantic import BaseModel



class FriendRequestCreate(BaseModel):
    user_id: UUID
    friend_id: UUID

class FriendRequestRead(BaseModel):
    id: UUID
    username: str
    surname: str
    name: str
    patronymic: Optional[str]
    photo: Optional[str]