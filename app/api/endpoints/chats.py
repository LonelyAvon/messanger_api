from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.authorization.func import (
    get_current_user,
)
from app.api.schemas.chat import (
    ChatCreate,
    ChatInfo,
    ChatPreview,
    ChatRead,
)
from app.api.schemas.user import UserRead
from app.api.services.chat import ChatService
from app.db.db import get_session

router = APIRouter(prefix="/chats", tags=["Чаты"])


@router.post(
    "/create_chat",
    response_model=ChatRead,
)
async def create_chat(
    chat: ChatCreate,
    session: AsyncSession = Depends(get_session),
    user: UserRead = Depends(get_current_user),
):
    result = await ChatService(session).create(chat)
    return result


@router.get("/my", response_model=list[ChatPreview], summary="Получение списка чатов")
async def get_chats(
    session: AsyncSession = Depends(get_session),
    user: UserRead = Depends(get_current_user),
):
    chats: list[ChatPreview] = await ChatService(session).get_chats(user_id=user.id)
    return chats


@router.get(
    "/messages/{chat_id}",
    response_model=ChatInfo,
)
async def get_chats_messages(
    chat_id: UUID,
    session: AsyncSession = Depends(get_session),
    user: UserRead = Depends(get_current_user),
):
    messages = await ChatService(session).get_messages(chat_id=chat_id, user_id=user.id)
    return messages
