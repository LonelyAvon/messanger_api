from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.chat import (
    ChatCreate,
    ChatInfo,
    ChatMessage,
    ChatPreview,
    ChatRead,
)
from app.api.schemas.user_chat import UserChatCreate
from app.api.services.user_chat import UserChatService
from app.db.db import get_session
from app.db.repositories.chat import ChatRepository
from app.db.repositories.chat_message import ChatMessageRepository


class ChatService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_chat_by_id(self, chat_id: UUID) -> ChatRead:
        chat: ChatRead = await ChatRepository(self.session).get_by_id(chat_id)
        return chat

    async def create(self, chat: ChatCreate) -> ChatRead:
        created_chat: ChatRead = await ChatRepository(self.session).create(
            type=chat.type, name=chat.name
        )
        for user_id in chat.users:
            user_chat_to_create: UserChatCreate = UserChatCreate(
                chat_id=created_chat.id, user_id=user_id
            )
            await UserChatService(self.session).create(user_chat_to_create)
        await self.session.commit()
        return created_chat

    async def find_chat_by_users(self, users: list[UUID], name: str) -> ChatRead:
        chat = await ChatRepository(self.session).get_by_users(users=users, name=name)
        return chat

    async def get_chats(self, user_id: UUID) -> list[ChatPreview]:
        chats = await ChatRepository(self.session).get_chats(user_id=user_id)
        response_chat: list[ChatPreview] = []
        for chat in chats:
            chat_preview: ChatPreview = ChatPreview(
                id=chat.id, chat_name=chat.chat_name, photo=chat.photo, type=chat.type
            )

            last_message_chat = await ChatRepository(
                self.session
            ).get_last_message_by_chat_id(chat_id=chat.id)
            if last_message_chat:
                last_message = ChatMessage(**last_message_chat)
                chat_preview.last_message = last_message
            response_chat.append(chat_preview)
        return response_chat

    async def get_messages(self, chat_id: UUID, user_id: UUID):
        chat = await ChatRepository(self.session).get_chat(
            chat_id=chat_id, user_id=user_id
        )
        messages: list[ChatMessage] = await ChatMessageRepository(
            self.session
        ).get_chat_messages(chat_id=chat_id)
        chat_info: ChatInfo = ChatInfo(
            id=chat.id, chat_name=chat.chat_name, photo=chat.photo, messages=messages
        )
        return chat_info
