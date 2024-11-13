from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class UserCreate(BaseModel):
    username: str
    password: str
    surname: str
    name: str
    patronymic: Optional[str] = None

class UserRead(BaseModel):
    id: UUID
    username: str
    surname: str
    name: str
    patronymic: Optional[str] = None

    email: Optional[str]
    is_verified_email: bool = False

    role: Optional[str] = "user"
    is_archived: Optional[bool] = False
    last_visit: Optional[datetime]
    photo: Optional[str] = None


class UserUpdate(BaseModel):
    username: Optional[str] = None
    surname: Optional[str] = None
    name: Optional[str] = None
    patronymic: Optional[str] = None

    email: Optional[str] = None


    def to_dict(self):
        # Создаем словарь и исключаем поля со значением None
        return self.model_dump(exclude_none=True)

class UserAuthorization(BaseModel):
    username: str
    password: str



class ChatUser(BaseModel):
    id: UUID
    surname: str
    name: str
    patronymic: Optional[str] = None
    photo: Optional[str] = None

    class Config:
        from_attributes = True 
