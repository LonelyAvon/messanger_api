from sqlalchemy import select
from app.db.repositories.abstract_repo import AbstractRepository

from app.db.models.user_chat import UserChat


class UserChatRepository(AbstractRepository):
    model =  UserChat
