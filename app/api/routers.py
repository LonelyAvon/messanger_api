from fastapi.routing import APIRouter
from .authorization import auto


api_router = APIRouter()
api_router.include_router(auto.router)
