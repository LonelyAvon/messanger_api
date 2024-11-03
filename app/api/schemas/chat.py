from uuid import UUID
from pydantic import BaseModel


class ChatCreate(BaseModel):
    name: str

class ChatRead(BaseModel):
    id: UUID
    name: str