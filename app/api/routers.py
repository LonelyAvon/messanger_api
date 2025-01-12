from fastapi.routing import APIRouter
from .authorization import auto
from .endpoints import chats, users, news


api_router = APIRouter()
api_router.include_router(auto.router)
api_router.include_router(users.router)
api_router.include_router(chats.router)
api_router.include_router(news.router)