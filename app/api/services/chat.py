from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.chat import ChatCreate, ChatRead
from app.api.schemas.user_chat import UserChatCreate
from app.api.services.user_chat import UserChatService
from app.db.repositories.chat import ChatRepository


class ChatService:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_chat_by_id(self, chat_id: UUID) -> ChatRead:
        chat: ChatRead = await ChatRepository(self.session).get_by_id(chat_id)
        return chat

    async def create(self, chat: ChatCreate) -> ChatRead:
        created_chat: ChatRead = await ChatRepository(self.session).create(**chat.model_dump(exclude={"users"}))
        for user_id in chat.users:
            user_chat_to_create: UserChatCreate = UserChatCreate(chat_id=created_chat.id, user_id=user_id)
            await UserChatService(self.session).create(user_chat_to_create)
        return created_chat
    
    async def find_chat_by_users(self, users: list[UUID], name: str) -> ChatRead:
        chat = await ChatRepository(self.session).get_by_users(users=users, name=name)
        return chat

    async def get_chats(self, user_id: UUID) -> list[ChatRead]:
        chats = await ChatRepository(self.session).get_chats(user_id=user_id)
        return chats
    