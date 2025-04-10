from uuid import UUID

from sqlalchemy import select

from app.db.models.friends import Friends
from app.db.models.user import User
from app.db.repositories.abstract_repo import AbstractRepository


class FriendRepository(AbstractRepository):
    model = Friends

    async def get_my_friends(self, user_id: UUID):
        query = (
            select(
                self.model.id,
                User.username,
                User.surname,
                User.name,
                User.patronymic,
                User.photo,
            )
            .where(self.model.user_id == user_id)
            .join(User, User.id == self.model.friend_id)
        )
        friends = await self._session.execute(query)
        return friends.mappings().all()

    async def get_my_friend(self, user_id: UUID, friend_id: UUID):
        query = (
            select(
                self.model.id,
                User.username,
                User.surname,
                User.name,
                User.patronymic,
                User.photo,
            )
            .where(self.model.user_id == user_id)
            .where(self.model.friend_id == friend_id)
            .join(User, User.id == self.model.friend_id)
        )
        friend = await self._session.execute(query)
        return friend.mappings().first()
