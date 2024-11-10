from datetime import datetime, timedelta, timezone
import json
from uuid import UUID
from fastapi import Depends, HTTPException, Request, APIRouter, Response
from fastapi.security import HTTPBearer
from app.api.schemas.chat import ChatCreate, ChatInfo, ChatMessage, ChatRead, ChatPreview, RedisChatMessage
from app.api.schemas.news import News
from app.api.schemas.token import Token
from app.api.schemas.user import UserRead, ChatUser
from app.api.services.chat import ChatService
from app.api.services.news import NewsService
from app.api.services.user import UserService
from app.api.utils.async_connector import AsyncHttpClient, get_client
from app.db.db import get_session
from sqlalchemy.ext.asyncio import AsyncSession
import app.api.authorization.utils.utils as utils
from app.api.authorization.func import get_current_user, validate_current_user, refresh_acess_token
from app.redis.redis import get_redis
from redis.asyncio.client import Redis # type: ignore


router = APIRouter(prefix="/news", tags=["Новостная лента"])


@router.get(
    "",
    response_model=News,
    summary="Получение новостной ленты"
)
async def get_news_feed(client: AsyncHttpClient = Depends(get_client), user: UserRead = Depends(get_current_user)):
    news: News = await NewsService(client).get_news_feed()
    return news    
