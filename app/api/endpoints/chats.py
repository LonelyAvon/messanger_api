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
)
async def create_chat(
    chat: ChatCreate,
    session: AsyncSession=Depends(get_session),
    user: UserRead = Depends(get_current_user)
    ):
    result = await ChatService(session).create(
        chat
    )
    return result

@router.get(
    "/my",
    response_model=list[ChatPreview],
    summary="Получение списка чатов"
    )
async def get_chats(
    session: AsyncSession=Depends(get_session), 
    user: UserRead = Depends(get_current_user)):

    chats: list[ChatPreview] = await ChatService(session).get_chats(user_id=user.id)
    return chats



@router.get(
        "/messages/{chat_id}", 
        response_model=ChatInfo,
        )
async def get_chats(
    chat_id: UUID, 
    session: AsyncSession=Depends(get_session), 
    user: UserRead = Depends(get_current_user)):
    messages = await ChatService(session).get_messages(chat_id=chat_id)
    return messages


