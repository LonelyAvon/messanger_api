from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.chat import ChatCreate, ChatRead
from app.api.schemas.chat_message import ChatMessageCreate
from app.api.schemas.user_chat import UserChatCreate
from app.api.services.user_chat import UserChatService
from app.db.db import get_session
from app.db.repositories.chat_message import ChatMessage, ChatMessageRepository


class ChatMessageService:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def create(self, chat_message: ChatMessageCreate):
        result = await ChatMessageRepository(self.session).create(**chat_message.model_dump())
        result = await self.get_message(result.id)
        await self.session.commit()
        return result
    
    async def get_message(self, message_id: UUID):
        result = await ChatMessageRepository(self.session).get_message(message_id)
        return result