from uuid import UUID
from fastapi import HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.user import UserRead, ChatUser
from app.db.repositories.user_repo import UserRepository
from app.settings import settings
import aiofiles


class UserService:

    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_user_by_id(self, user_id: UUID) -> UserRead:
        user: UserRead = await UserRepository(self.session).get_by_id(user_id)
        return user
    
    async def upload_photo(self, user_id: UUID, file: UploadFile):
        file_path = f"photos/{user_id}.{file.filename.split('.')[-1]}"
        user: UserRead = await UserRepository(self.session).update_one(user_id, photo=settings.get_domen + "/" + file_path)
        async with aiofiles.open(file_path, "wb") as out_file:
            content = await file.read()  # async read
            await out_file.write(content)  # async write
        
        await UserRepository(self.session).commit()
        return user