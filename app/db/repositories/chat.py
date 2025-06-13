from uuid import UUID

from sqlalchemy import and_, case, func, or_, select
from sqlalchemy.orm import aliased, joinedload
from sqlalchemy.sql.functions import coalesce

from app.api.schemas.chat import ChatRead
from app.db.models.chat import Chat
from app.db.models.chat_message import ChatMessage
from app.db.models.user import User
from app.db.models.user_chat import UserChat
from app.db.repositories.abstract_repo import AbstractRepository


class ChatRepository(AbstractRepository):
    model = Chat

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

    async def get_chats(self, user_id: UUID) -> list[ChatRead]:
        # Подзапрос для собеседника в личных чатах
        interlocutor_subq = (
            select(UserChat.user_id)
            .where((UserChat.chat_id == self.model.id) & (UserChat.user_id != user_id))
            .correlate(self.model)
            .limit(1)
            .scalar_subquery()
        )

        # Фото из последнего сообщения не от пользователя
        last_message_photo_subq = (
            select(User.photo)
            .select_from(ChatMessage)
            .join(User, User.id == ChatMessage.user_id)
            .where(
                (ChatMessage.chat_id == self.model.id)
                & (ChatMessage.user_id != user_id)
            )
            .order_by(ChatMessage.created_time.desc())
            .limit(1)
            .correlate(self.model)
            .scalar_subquery()
        )

        random_user_photo_subq = (
            select(User.photo)
            .select_from(UserChat)
            .join(User, User.id == UserChat.user_id)
            .where((UserChat.chat_id == self.model.id))
            .order_by(func.random())
            .limit(1)
            .correlate(self.model)
            .scalar_subquery()
        )

        # Комбинированное фото для группы
        group_photo = coalesce(last_message_photo_subq, random_user_photo_subq).label(
            "group_photo"
        )

        query = (
            select(
                self.model.id,
                case(
                    (
                        self.model.type == "personal",
                        func.concat_ws(" ", User.surname, User.name, User.patronymic),
                    ),
                    else_=self.model.name,
                ).label("chat_name"),
                case(
                    (self.model.type == "personal", User.photo),
                    (self.model.type == "group", group_photo),
                    else_=User.photo,
                ).label("photo"),
                self.model.type,
            )
            .join(UserChat, UserChat.chat_id == self.model.id)
            .outerjoin(
                User, and_(self.model.type == "personal", User.id == interlocutor_subq)
            )
            .where(UserChat.user_id == user_id)
            .group_by(self.model.id, User.id)
            .distinct()
        )

        result = await self._session.execute(query)
        return result.mappings().all()

    async def get_chat(self, chat_id: UUID):
        query = (
            select(
                ChatMessage.id,
                ChatMessage.message,
                ChatMessage.file,
                ChatMessage.created_time,
                func.json_build_object(
                    "id",
                    User.id,
                    "name",
                    User.name,
                    "patronymic",
                    User.patronymic,
                    "surname",
                    User.surname,
                    "photo",
                    User.photo,
                ).label("user"),
            )
            .join(User, User.id == ChatMessage.user_id)
            .join(self.model, self.model.id == ChatMessage.chat_id)
            .where(ChatMessage.chat_id == chat_id)
            .order_by(ChatMessage.created_time)
        )
        result = await self._session.execute(query)
        return result.mappings().all()

    async def get_last_message_by_chat_id(self, chat_id: UUID):
        last_message_subquery = (
            select(func.max(ChatMessage.created_time).label("last_message_time"))
            .where(ChatMessage.chat_id == chat_id)
            .scalar_subquery()
        )

        query = (
            select(
                ChatMessage.message,
                ChatMessage.created_time,
                User.surname,
                User.name,
                User.patronymic,
                User.photo,
            )
            .join(User, User.id == ChatMessage.user_id)
            .where(ChatMessage.chat_id == chat_id)
            .where(ChatMessage.created_time == last_message_subquery)
        )

        result = await self._session.execute(query)
        last_message = result.mappings().first()
        return last_message

    # async def get_chat(self, chat_id: UUID):
    #     query = (
    #         select(
    #             self.model.id,
    #             self.model.name.label("chat_name"),
    #         )
    #         .where(self.model.id == chat_id)
    #     )

    #     result = await self._session.execute(query)
    #     chat = result.mappings().first()
    #     return chat
