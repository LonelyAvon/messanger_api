from uuid import UUID
from sqlalchemy import and_, func, select
from app.db.repositories.abstract_repo import AbstractRepository

from app.db.models.chat import Chat
from app.db.models.user_chat import UserChat


class ChatRepository(AbstractRepository):
    model =  Chat


    async def get_by_users(self, users: list[UUID], name: str):
        query = (
        select(self.model)
        .join(UserChat, UserChat.chat_id == self.model.id)
        .where(and_(UserChat.user_id.in_(users), self.model.name == name))
        .group_by(self.model.id)
        .having(func.count(UserChat.user_id) == len(users))
        )

        result = await self._session.execute(query)
        return result.scalars().first()