from datetime import datetime, timedelta, timezone
import json
from uuid import UUID
from fastapi import Depends, HTTPException, Request, APIRouter, Response
from fastapi.security import HTTPBearer
from app.api.schemas.chat import ChatCreate
from app.api.schemas.token import Token
from app.api.schemas.user import UserRead
from app.api.utils.static import get_chat_name_by_2_persons
from app.db.db import get_session
from sqlalchemy.ext.asyncio import AsyncSession
import app.api.authorization.utils.utils as utils
from app.api.authorization.func import get_current_user, validate_current_user, refresh_acess_token
from app.redis.redis import get_redis
from redis.asyncio.client import Redis # type: ignore


router = APIRouter(prefix="/chats", tags=["Чаты"])


@router.post(
    "/create_chat/{user_id}", 
    response_model=ChatCreate,
    summary="Создание чата 2 пользователей"
    )
async def create_chat(
    user_id: UUID, 
    chat: ChatCreate, 
    redis: Redis = Depends(get_redis), 
    user: UserRead = Depends(get_current_user)):

    chat_name = get_chat_name_by_2_persons(user.id, user_id)

    if await redis.exists(chat_name):
        raise HTTPException(status_code=400, detail="Chat already exists")
    # Создание нового чата
    await redis.rpush(chat_name, json.dumps({"message": "Chat created"}))
    return chat

@router.get("/chats/")
async def get_chats(redis: Redis = Depends(get_redis)):
    chats = await redis.keys("chat:*")
    return {"chats": [chat.decode("utf-8") for chat in chats]}

@router.get("/messages/{chat_id}")
async def get_chats(chat_id: str ,redis: Redis = Depends(get_redis)):
    chat = await redis.exists(f"chat:{chat_id}")
    if chat == 0:
        raise HTTPException(status_code=404, detail="Chat not found")
    messages = await redis.lrange(f"chat:{chat_id}", 0, -1)
    return {"chat_id": chat_id, "messages": [json.loads(message.decode("utf-8")) for message in messages]}

# @app.get("/messages/{chat_id}")
# async def get_messages(chat_id: str):
#     messages = await redis.lrange(f"chat:{chat_id}", 0, -1)
#     return {"chat_id": chat_id, "messages": [message.decode("utf-8") for message in messages]}