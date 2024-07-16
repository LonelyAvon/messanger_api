from fastapi import Depends, Form, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer
from app.api.authorization.utils.utils import validate_password, decode_jwt
from app.db.db import get_session
from app.db.repositories.user_repository.user_repo import UserRepository
from app.settings import settings


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
    
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(OAuth2PasswordBearer(tokenUrl=f"{settings.fast_api_prefix}/auth/login"))):
    token = credentials.credentials
    decoded = decode_jwt(token)
    async for session in get_session():
        user = await UserRepository(session).get_by_id(decoded["sub"])
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user