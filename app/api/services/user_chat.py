from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.user import UserRead
from app.api.schemas.user_chat import  UserChatCreate, UserChatRead
from app.db.repositories.user_chat import  UserChatRepository
from app.db.repositories.user_repo import UserRepository


class UserChatService:

    def __init__(self, session: AsyncSession):
        self.session = session


    async def create(self, user_chat: UserChatCreate) -> UserChatRead:
        user: UserRead = await UserRepository(self.session).get_by_filter_one(id=user_chat.user_id, is_archived=False)
        if user is None:
            raise HTTPException(status_code=404, detail=f"User {user_chat.user_id} not found")

        created_user_chat: UserChatRead = await UserChatRepository(self.session).create(**user_chat.model_dump())

        return created_user_chat
    