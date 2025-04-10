from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.authorization.func import get_current_user
from app.api.schemas.friend_request import FriendRequestRead
from app.api.schemas.user import UserRead
from app.api.services.friend import FriendService
from app.api.services.friend_requests import FriendRequestsService
from app.api.services.user import UserService
from app.db.db import get_session

router = APIRouter(prefix="/friends", tags=["Друзья"])


@router.get("/find")
async def find_friends(
    query: Optional[str] = Query(None, description="Поиск по ФИО и юзернейму"),
    session: AsyncSession = Depends(get_session),
    user: UserRead = Depends(get_current_user),
):
    """
    Поиск по имени фамилии и отчеству одновременно
    """
    users = await UserService(session).find_users(query, user.id)
    return users


@router.get("/my", response_model=list[FriendRequestRead])
async def get_friends(
    session: AsyncSession = Depends(get_session),
    user: UserRead = Depends(get_current_user),
):
    friends = await FriendService(session).get_my_friends(user.id)
    return friends


@router.get("/requests/my", response_model=list[FriendRequestRead])
async def get_requests_my(
    session: AsyncSession = Depends(get_session),
    user: UserRead = Depends(get_current_user),
):
    requests = await FriendRequestsService(session).get_my_requests(user.id)
    return requests


@router.get("/requests/for_me", response_model=list[FriendRequestRead])
async def get_requests_for_me(
    session: AsyncSession = Depends(get_session),
    user: UserRead = Depends(get_current_user),
):
    requests = await FriendRequestsService(session).get_for_me_requests(user.id)
    return requests


@router.post("/requests/{friend_id}", response_model=FriendRequestRead)
async def send_request(
    friend_id: UUID,
    session: AsyncSession = Depends(get_session),
    user: UserRead = Depends(get_current_user),
):
    request = await FriendRequestsService(session).send_request(user.id, friend_id)
    return request


@router.post("/requests/{request_id}/accept")
async def accept_request(
    request_id: UUID,
    session: AsyncSession = Depends(get_session),
    user: UserRead = Depends(get_current_user),
):
    request = await FriendRequestsService(session).accept_request(request_id, user.id)
    return request


@router.post("/requests/{request_id}/reject")
async def reject_request(
    request_id: UUID,
    session: AsyncSession = Depends(get_session),
    user: UserRead = Depends(get_current_user),
):
    request = await FriendRequestsService(session).reject_request(request_id)
    return request
