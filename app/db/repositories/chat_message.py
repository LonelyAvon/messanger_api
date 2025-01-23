from uuid import UUID
from sqlalchemy import and_, func, select
from sqlalchemy.orm import aliased
from app.api.schemas.chat import ChatRead
from app.db.models.user import User
from app.db.repositories.abstract_repo import AbstractRepository

from app.db.models.chat_message import ChatMessage


class ChatMessageRepository(AbstractRepository):
    model =  ChatMessage

    async def get_message(self, id):
        query = (
            select(User.surname, User.name, ChatMessage.message, ChatMessage.created_time)
            .where(ChatMessage.id == id)
            .join(ChatMessage.user)
            )
        result = await self._session.execute(query)
        return result.mappings().first()
    

    async def get_chat_messages(self, chat_id: UUID):
        query = (
            select(
                ChatMessage.message,
                ChatMessage.created_time,
                User.surname,
                User.name,
                User.patronymic,
                User.photo,
            )
            .join(User, User.id == ChatMessage.user_id)
            .where(ChatMessage.chat_id == chat_id)
            .order_by(ChatMessage.created_time)
        )

        result = await self._session.execute(query)
        chat_messages = result.mappings().all()
        return chat_messages