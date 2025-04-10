from uuid import UUID

from sqlalchemy import and_, func, select
from sqlalchemy.orm import aliased

from app.api.schemas.chat import ChatRead
from app.db.models.chat_message import ChatMessage
from app.db.models.user import User
from app.db.repositories.abstract_repo import AbstractRepository


class ChatMessageRepository(AbstractRepository):
    model = ChatMessage

    async def get_message(self, id):
        query = (
            select(
                User.id.label("sender_id"),
                ChatMessage.message,
                ChatMessage.created_time,
                User.surname,
                User.name,
                User.patronymic,
                User.photo,
            )
            .join(User, User.id == ChatMessage.user_id)
            .where(ChatMessage.id == id)
        )
        result = await self._session.execute(query)
        return result.mappings().first()

    async def get_chat_messages(self, chat_id: UUID):
        query = (
            select(
                User.id.label("sender_id"),
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
