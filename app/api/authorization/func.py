from datetime import datetime, timezone
from fastapi import Depends, Form, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer
from app.api.authorization.utils.utils import validate_password, decode_jwt, encode_jwt, create_token
from app.api.schemas.user import UserRead
from app.db.db import get_session
from app.db.repositories.user_repo import UserRepository
from app.settings import settings
from app.api.schemas.token import Token


async def validate_current_user(username: str = Form(), password: str = Form()):
    async for session in get_session():
        user: UserRead = await UserRepository(session).get_user_by_username(username)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not validate_password(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid password")
        if user.is_archived:
            raise HTTPException(status_code=401, detail="User is archived")
        return user
    
async def get_current_user(access_token: HTTPAuthorizationCredentials = Depends(OAuth2PasswordBearer(tokenUrl=f"{settings.FAST_API_PREFIX}/auth/login"))):
    decoded = decode_jwt(access_token)
    if decoded.get('token_type') is None:
        raise HTTPException(status_code=401, detail="Invalid token type")
    if decoded['token_type'] != 'access':
        raise HTTPException(status_code=401, detail="Invalid token type")
    async for session in get_session():
        user: UserRead = await UserRepository(session).get_by_id(decoded["sub"])
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        updated_user: UserRead = await UserRepository(session).update_one(user.id, last_visit=datetime.now(timezone.utc))
        await UserRepository(session).commit()
        return updated_user

async def refresh_acess_token(request: Request):
    cookies = request.cookies
    refresh_token = cookies.get("refresh_token", None)
    if refresh_token is None:
        raise HTTPException(status_code=401, detail="Unhauthorized")
    
    decoded = decode_jwt(refresh_token)
    if decoded.get('token_type', None) is None:
        raise HTTPException(status_code=401, detail="Invalid token type")
    if decoded['token_type'] != 'refresh':
        raise HTTPException(status_code=401, detail="Invalid token type")
    
    async for session in get_session():
        user: UserRead = await UserRepository(session).get_by_id(decoded["sub"])
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        if user.is_archived:
            raise HTTPException(status_code=401, detail="User is archived")
        access_token = encode_jwt(payload=create_token("access", {"sub": str(user.id), "username": user.username, "role": user.role}))
        return Token(access_token=access_token)
