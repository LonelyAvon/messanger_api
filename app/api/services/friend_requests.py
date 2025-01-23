from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.friend_requests import FriendRequestsRepository





class FriendRequestsService:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_my_requests(self, user_id: UUID):
        requests = await FriendRequestsRepository(self.session).get_my_requests(user_id)
        return requests
    
    async def get_for_me_requests(self, user_id: UUID):
        requests = await FriendRequestsRepository(self.session).get_for_me_requests(user_id)
        return requests
    
    async def send_request(self, user_id: UUID, friend_id: UUID):
        request = await FriendRequestsRepository(self.session).create(user_id=user_id, friend_id=friend_id)
        request = await FriendRequestsRepository(self.session).get_request(request.id)
        await self.session.commit()
        return request