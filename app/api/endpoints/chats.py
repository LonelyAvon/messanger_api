from datetime import datetime, timedelta, timezone
import json
from uuid import UUID
from fastapi import Depends, HTTPException, Request, APIRouter, Response
from fastapi.security import HTTPBearer
from app.api.schemas.chat import ChatCreate, ChatMessage, ChatRead
from app.api.schemas.token import Token
from app.api.schemas.user import UserRead
from app.api.services.chat import ChatService
from app.api.utils.static import get_chat_name_by_2_persons
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
    chat_message: ChatMessage = ChatMessage(
        user=None,
        message=f"Ваш чат был создан!"
    )
    await redis.rpush(str(created_chat.id), chat_message.model_dump_json())
    await session.commit()
    return created_chat

@router.get("/chats")
async def get_chats(redis: Redis = Depends(get_redis), user: UserRead = Depends(get_current_user)):
    chats = await redis.keys("chat:*")
    return {"chats": [chat.decode("utf-8") for chat in chats]}

@router.get("/messages/{chat_id}")
async def get_chats(chat_id: UUID ,redis: Redis = Depends(get_redis)):
    chat = await redis.exists(str(chat_id))
    if chat == 0:
        raise HTTPException(status_code=404, detail="Chat not found")
    messages = await redis.lrange(str(chat_id), 0, -1)
    return {"chat_id": chat_id, "messages": [json.loads(message.decode("utf-8")) for message in messages]}

# @app.get("/messages/{chat_id}")
# async def get_messages(chat_id: str):
#     messages = await redis.lrange(f"chat:{chat_id}", 0, -1)
#     return {"chat_id": chat_id, "messages": [message.decode("utf-8") for message in messages]}