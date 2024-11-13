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
from app.api.schemas.user import UserRead, UserUpdate
from app.api.utils.static import get_chat_name_by_2_persons
from app.db.db import get_session
from sqlalchemy.ext.asyncio import AsyncSession
import app.api.authorization.utils.utils as utils
from app.api.authorization.func import get_current_user, validate_current_user, refresh_acess_token
from app.db.repositories.user_repo import UserRepository
from app.redis.redis import get_redis
from redis.asyncio.client import Redis # type: ignore
from app.db.db import async_session



router = APIRouter(prefix="/user", tags=["Пользовательское взаимодействие"])


@router.get(
    "/me", 
    response_model=UserRead, 
    summary="Получение информации о текущем пользователе")
async def read_users_me(current_user: UserRead = Depends(get_current_user)):
    return current_user

@router.put(
    "/update",
    response_model=UserRead,
    summary="Обновление информации о пользователе")
async def update_user(user_update: UserUpdate, user: UserRead = Depends(get_current_user), session: AsyncSession=Depends(get_session)):
    user: UserRead = await UserService(session).update_user(user.id, user_update)
    return user


@router.post(
    "/photo",
    response_model=UserRead,
    summary="Загрузка фото профиля")
async def upload_photo(file: UploadFile = File(...), user: UserRead = Depends(get_current_user), session: AsyncSession=Depends(get_session)):
    user: UserRead = await UserService(session).upload_photo(user.id, file)
    return user

@router.post(
    "/email/verify",
    summary="Проверка почты")
async def email_send_verified_message(request: Request, user: UserRead = Depends(get_current_user), session: AsyncSession=Depends(get_session)):
    """
    Отправка сообщение с ссылкой на потдверждение почты
    """
    token = request.headers.get("Authorization").split()[-1]
    await UserService(session).send_message(user.email, "Ссылка", f"Ваша ссылка для потдверждения почты: \n{settings.get_domen}/user/email/{token}")
    return f"Ссылка с потдверждение отправлена на почту {user.email}"

@router.get(
    "/email/{token}",
    response_model=UserRead,
    summary="Проверка почты",
    include_in_schema=False)
async def email_verified(token: str, session: AsyncSession = Depends(get_session)):
    """
    Потдверждение почты с помощью ссылки
    """
    user: UserRead = await UserService(session).verified_email_by_token(token)
    return user

@router.post(
    '/password/reset/email',
    summary="Сброс пароля по почте")
async def password_reset(user: UserRead = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    user: UserRead = await UserService(session).reset_password_by_email(user)
    return "Пароль сброшен. Вам на почту отправлен новый пароль"

@router.post(
    "/password/reset/old_password",
    summary="Сброс пароля по старому паролю")
async def password_reset(old_password: str, new_password: str, user: UserRead = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    user: UserRead = await UserService(session).reset_password_by_old_password(user, old_password, new_password)
    return "Пароль сброшен"