from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.services.friend import FriendService
from app.db.repositories.friend_requests import FriendRequestsRepository


class FriendRequestsService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_my_requests(self, user_id: UUID):
        requests = await FriendRequestsRepository(self.session).get_my_requests(user_id)
        return requests

    async def get_for_me_requests(self, user_id: UUID):
        requests = await FriendRequestsRepository(self.session).get_for_me_requests(
            user_id
        )
        return requests

    async def send_request(self, user_id: UUID, friend_id: UUID):
        request = await FriendRequestsRepository(self.session).create(
            user_id=user_id, friend_id=friend_id
        )
        request = await FriendRequestsRepository(self.session).get_request(request.id)
        await self.session.commit()
        return request

    async def accept_request(self, request_id: UUID, user_id: UUID):
        request = await FriendRequestsRepository(self.session).delete_request(
            request_id
        )
        if request is None:
            raise HTTPException(status_code=404, detail="Заявка уже принята")
        first_friend = await FriendService(self.session).add_friend(
            user_id=request.user_id, friend_id=request.friend_id
        )
        second_friend = await FriendService(self.session).add_friend(
            user_id=request.friend_id, friend_id=request.user_id
        )
        await self.session.commit()
        if first_friend.user_id == user_id:
            friend = await FriendService(self.session).get_my_friend(
                user_id=user_id, friend_id=first_friend.friend_id
            )
            return friend
        else:
            friend = await FriendService(self.session).get_my_friend(
                user_id=second_friend.friend_id, friend_id=user_id
            )
            return friend

    async def reject_request(self, request_id: UUID):
        request = await FriendRequestsRepository(self.session).delete_request(
            request_id
        )
        await self.session.commit()
        return request
