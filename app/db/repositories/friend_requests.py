from uuid import UUID

from sqlalchemy import delete, select

from app.db.models.friends import FriendRequests
from app.db.models.user import User
from app.db.repositories.abstract_repo import AbstractRepository


class FriendRequestsRepository(AbstractRepository):
    model = FriendRequests

    async def get_my_requests(self, user_id: UUID):
        query = (
            select(
                self.model.id,
                User.username,
                User.surname,
                User.name,
                User.patronymic,
                User.photo,
            )
            .where(FriendRequests.user_id == user_id)
            .join(User, User.id == FriendRequests.friend_id)
            .select_from(FriendRequests)
        )

        result = await self._session.execute(query)
        return result.mappings().all()

    async def get_for_me_requests(self, user_id: UUID):
        query = (
            select(
                self.model.id,
                User.username,
                User.surname,
                User.name,
                User.patronymic,
                User.photo,
            )
            .where(FriendRequests.friend_id == user_id)
            .join(User, User.id == FriendRequests.user_id)
            .select_from(FriendRequests)
        )

        result = await self._session.execute(query)
        return result.mappings().all()

    async def get_request(self, id: UUID):
        query = (
            select(
                self.model.id,
                User.username,
                User.surname,
                User.name,
                User.patronymic,
                User.photo,
            )
            .where(FriendRequests.id == id)
            .join(User, User.id == FriendRequests.friend_id)
            .select_from(FriendRequests)
        )

        result = await self._session.execute(query)
        return result.mappings().first()

    async def delete_request(self, request_id: UUID):
        query = (
            delete(self.model).where(self.model.id == request_id).returning(self.model)
        )
        result = await self._session.execute(query)
        request = result.scalars().first()
        return request
