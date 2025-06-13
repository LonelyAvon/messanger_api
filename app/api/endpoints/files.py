import uuid
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, File, Query, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.authorization.func import get_current_user
from app.api.schemas.friend_request import FriendRequestRead
from app.api.schemas.user import UserRead
from app.api.services.friend import FriendService
from app.api.services.friend_requests import FriendRequestsService
from app.api.services.user import UserService
from app.api.utils.minio_connector import MinioClient
from app.db.db import get_session

router = APIRouter(prefix="/files", tags=["Файлы"])


@router.post("/{chat_id}/upload")
async def upload_photo(
    chat_id: UUID,
    minio: MinioClient,
    file: UploadFile = File(...),
    user: UserRead = Depends(get_current_user),
):
    id = uuid.uuid4()
    extension = file.filename.split(".")[-1]
    file_path = f"{id}.{extension}"
    filepath = await minio.upload_file(
        bucket_name=str(chat_id),
        file_data=await file.read(),
        file_path=file_path,
    )

    return {"filePath": filepath}
