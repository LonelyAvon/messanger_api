from fastapi import Depends, Form, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer
from app.api.authorization.utils.utils import validate_password, decode_jwt, encode_jwt, create_token
from app.db.db import get_session
from app.db.repositories.user_repository.user_repo import UserRepository
from app.settings import settings
from app.api.schemas.token import Token


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
    
async def get_current_user(access_token: HTTPAuthorizationCredentials = Depends(OAuth2PasswordBearer(tokenUrl=f"{settings.fast_api_prefix}/auth/login"))):
    decoded = decode_jwt(access_token)
    if decoded.get('token_type'):
        raise HTTPException(status_code=401, detail="Invalid token type")
    if decoded['token_type'] != 'access':
        raise HTTPException(status_code=401, detail="Invalid token type")
    async for session in get_session():
        user = await UserRepository(session).get_by_id(decoded["sub"])
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

async def refresh_acess_token(refresh_token: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False))):
    decoded = decode_jwt(refresh_token.credentials)
    if decoded.get('token_type'):
        raise HTTPException(status_code=401, detail="Invalid token type")
    if decoded['token_type'] != 'refresh':
        raise HTTPException(status_code=401, detail="Invalid token type")
    
    async for session in get_session():
        user = await UserRepository(session).get_by_id(decoded["sub"])
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if user.is_archived:
            raise HTTPException(status_code=401, detail="User is archived")
        access_token = encode_jwt(payload=create_token("access", {"sub": str(user.id), "username": user.username}))
        return Token(access_token=access_token, refresh_token=refresh_token.credentials)
