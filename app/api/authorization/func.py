from fastapi import Form, HTTPException

from app.api.authorization.utils.utils import validate_password
from app.db.db import get_session
from app.db.repositories.user_repository.user_repo import UserRepository


async def validate_current_user(username: str = Form(), password: str = Form()):
    async for session in get_session():
        user = await UserRepository(session).get_user_by_username(username)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not validate_password(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid password")
        if user.is_archived:
            raise HTTPException(status_code=401, detail="User is archived")
        return user