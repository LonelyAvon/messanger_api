from typing import Optional
from uuid import UUID

from pydantic import BaseModel, field_validator

from app.settings import settings


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

    @field_validator("photo")
    def validate_photo(cls, v: str):
        if v:
            return f"{settings.DOMEN}/{v}"
        return v
