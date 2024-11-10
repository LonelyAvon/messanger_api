from datetime import datetime, timedelta, timezone
import json
from uuid import UUID
from fastapi import Depends, HTTPException, Request, APIRouter, Response
from fastapi.security import HTTPBearer
from app.api.schemas.chat import ChatCreate, ChatInfo, ChatMessage, ChatRead, ChatPreview, RedisChatMessage
from app.api.schemas.token import Token
from app.api.schemas.user import UserRead, ChatUser
from app.api.services.chat import ChatService
from app.api.services.user import UserService
from app.db.db import get_session
from sqlalchemy.ext.asyncio import AsyncSession
import app.api.authorization.utils.utils as utils
from app.api.authorization.func import get_current_user, validate_current_user, refresh_acess_token
from app.redis.redis import get_redis
from redis.asyncio.client import Redis # type: ignore


router = APIRouter(prefix="/chats", tags=["Чаты"])


@router.post(
    "/create_chat", 
    response_model=ChatRead,
    summary="Создание чатов"
    )
async def create_chat(
    chat: ChatCreate, 
    redis: Redis = Depends(get_redis), 
    session: AsyncSession=Depends(get_session),
    user: UserRead = Depends(get_current_user)):

    find_chat: ChatRead = await ChatService(session).find_chat_by_users(users=chat.users, name=chat.name)
    if find_chat:
        raise HTTPException(status_code=409, detail="Такой чат уже существует")

    created_chat: ChatRead = await ChatService(session).create(chat)
    chat_message: RedisChatMessage = RedisChatMessage(
        user_id=None,
        message=f"Ваш чат был создан!"
    )
    await redis.rpush(str(created_chat.id), chat_message.model_dump_json())
    messages = await redis.lrange(str(created_chat.id), 0, -1)
    for message in messages:
        print(message.decode("utf-8"))
    await session.commit()
    return created_chat

@router.get(
    "/my",
    response_model=list[ChatPreview],
    summary="Получение списка чатов"
    )
async def get_chats(
    redis: Redis = Depends(get_redis), 
    session: AsyncSession=Depends(get_session), 
    user: UserRead = Depends(get_current_user)):

    chats: list[ChatRead] = await ChatService(session).get_chats(user_id=user.id)

    answer: list[ChatPreview] = []

    for chat in chats:
        redis_message = await redis.lrange(str(chat.id), -1, -1)
        message: RedisChatMessage = RedisChatMessage(**json.loads(redis_message[0]))
        user_db = await UserService(session).get_user_by_id(user_id=message.user_id)

        if user_db:
            chat_user: ChatUser = ChatUser.model_validate(user_db)
        else:
            chat_user=None
            
        chat_message: ChatMessage = ChatMessage(
            user=chat_user,
            message=message.message

        )
        chat_preview: ChatPreview = ChatPreview(
            id=chat.id,
            name=chat.name,
            type=chat.type,
            last_message=chat_message
        )

        answer.append(chat_preview)

    return answer

@router.get("/messages/{chat_id}", response_model=ChatInfo)
async def get_chats(
    chat_id: UUID, 
    redis: Redis = Depends(get_redis), 
    session: AsyncSession=Depends(get_session), 
    user: UserRead = Depends(get_current_user)):

    redis_chat = await redis.exists(str(chat_id))
    if redis_chat == 0:
        raise HTTPException(status_code=404, detail="Chat not found")
    redis_messages = await redis.lrange(str(chat_id), 0, -1)


    chat: ChatRead = await ChatService(session).get_chat_by_id(chat_id=chat_id)
    chat_info: ChatInfo = ChatInfo(
        id=chat.id,
        name=chat.name,
        type=chat.type,
        messages=[]
    )
    for message in redis_messages:
        message: RedisChatMessage = RedisChatMessage(**json.loads(message))
        user_db = await UserService(session).get_user_by_id(user_id=message.user_id)
        if user_db:
            chat_user: ChatUser = ChatUser.model_validate(user_db)
        else:
            chat_user=None
        chat_message: ChatMessage = ChatMessage(
            user=chat_user,
            message=message.message
        )
        chat_info.messages.append(chat_message)
    # for message in messages:
    return chat_info

