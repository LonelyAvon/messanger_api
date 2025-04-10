from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.friend import FriendRepository


class FriendService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_my_friends(self, user_id: UUID):
        friends = await FriendRepository(self.session).get_my_friends(user_id)
        return friends

    async def get_my_friend(self, user_id: UUID, friend_id: UUID):
        friend = await FriendRepository(self.session).get_my_friend(user_id, friend_id)
        return friend

    async def add_friend(self, user_id: UUID, friend_id: UUID):
        friend = await FriendRepository(self.session).create(
            user_id=user_id, friend_id=friend_id
        )
        return friend
