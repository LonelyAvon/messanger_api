from datetime import datetime, timedelta, timezone
import json
import aiofiles
from uuid import UUID
from fastapi import Depends, File, HTTPException, Request, APIRouter, Response, UploadFile
from fastapi.security import HTTPBearer
from app.api.services.user import UserService
from app.settings import settings
from app.api.schemas.chat import ChatCreate
from app.api.schemas.token import Token
from app.api.schemas.user import UserRead
from app.api.utils.static import get_chat_name_by_2_persons
from app.db.db import get_session
from sqlalchemy.ext.asyncio import AsyncSession
import app.api.authorization.utils.utils as utils
from app.api.authorization.func import get_current_user, validate_current_user, refresh_acess_token
from app.db.repositories.user_repo import UserRepository
from app.redis.redis import get_redis
from redis.asyncio.client import Redis # type: ignore



router = APIRouter(prefix="/user", tags=["Пользовательское взаимодействие"])


@router.get(
    "/me", 
    response_model=UserRead, 
    summary="Получение информации о текущем пользователе")
async def read_users_me(current_user: UserRead = Depends(get_current_user)):
    return current_user

@router.post(
    "/photo",
    response_model=UserRead,
    summary="Загрузка фото профиля"
)
async def upload_photo(file: UploadFile = File(...), user: UserRead = Depends(get_current_user), session: AsyncSession=Depends(get_session)):
    user: UserRead = await UserService(session).upload_photo(user.id, file)
    return user