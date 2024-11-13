from uuid import UUID
from fastapi import HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.authorization.utils.utils import decode_jwt, validate_password
from app.api.schemas.user import UserRead, ChatUser, UserUpdate
from app.db.repositories.user_repo import UserRepository
from app.settings import settings
import aiofiles
from email.message import EmailMessage
import aiosmtplib
from passlib.pwd import genword


class UserService:

    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_user_by_id(self, user_id: UUID) -> UserRead:
        user: UserRead = await UserRepository(self.session).get_by_id(user_id)
        return user

    async def update_user(self, user_id, user: UserUpdate) -> UserRead:
        user: UserRead = await UserRepository(self.session).update_one(user_id, **user.to_dict())
        await UserRepository(self.session).commit()
        return user
    
    async def reset_password_by_email(self, user: UserRead):
        if not user.is_verified_email:
            raise HTTPException(status_code=404, detail="Ваша почта не верифицирована")
        new_password = genword(length=8)
        await self.send_message(user.email, "Восстановление пароля", f"Ваш новый пароль: {new_password}")
        user: UserRead = await UserRepository(self.session).update_password(new_password)
        await UserRepository(self.session).commit()
        return user    
    
    async def reset_password_by_old_password(self, user: UserRead, old_password, new_password):
        if not validate_password(old_password, user.password):
            raise HTTPException(status_code=404, detail="Неверный пароль")
        user: UserRead = await UserRepository(self.session).update_password(new_password)
        await UserRepository(self.session).commit()
        return user

    async def upload_photo(self, user_id: UUID, file: UploadFile):
        user: UserRead = await UserRepository(self.session).update_one(user_id, photo=settings.get_domen + "/" + file_path)
        file_path = f"photos/{user_id}.{file.filename.split('.')[-1]}"
        async with aiofiles.open(file_path, "wb") as out_file:
            content = await file.read()  # async read
            await out_file.write(content)  # async write
        
        await UserRepository(self.session).commit()
        return user
    
    async def send_message(self, email: str, theme: str, message: str):

        email_message: EmailMessage = EmailMessage()
        email_message["From"] = settings.SMTP_EMAIL
        email_message["To"] = email
        email_message["Subject"] = theme
        email_message.set_content(message)
        try:
            tmp = await aiosmtplib.send(
                email_message,
                hostname="smtp.mail.ru",
                port=465,
                use_tls=True,
                username=settings.SMTP_EMAIL,
                password=settings.SMTP_PASSWORD,
            )
            return tmp
        except Exception as e:
            raise HTTPException(status_code=404 , detail=f"EMail {email} not found")


    async def verified_email_by_token(self, token: str) -> UserRead:
        decoded = decode_jwt(token)
        user: UserRead = await UserRepository(self.session).get_by_id(decoded["sub"])
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        user: UserRead = await UserRepository(self.session).update_one(user.id, is_verified_email=True)
        await UserRepository(self.session).commit()
        return user
