from fastapi import Depends, HTTPException, Request, APIRouter
from app.api.schemas.user import(
    UserCreate, 
    UserRead,
)
from app.api.schemas.token import Token
from app.db.models.user import User
from app.db.db import get_session
from app.db.repositories.user_repository.user_repo import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
import app.api.authorization.utils.utils as utils
from .func import validate_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])



@router.post("/register", response_model=UserRead)
async def register(request: Request, user: UserCreate, session: AsyncSession=Depends(get_session)):
    user = await UserRepository(session).create(user)
    await UserRepository(session).commit()
    return user

@router.post("/login")
async def login(request: Request, user: UserRead = Depends(validate_current_user)):
    jwt_payload = {
        "sub": str(user.id),
        "username": user.username
    }
    token = utils.encode_jwt(jwt_payload)
    return Token(access_token=token)