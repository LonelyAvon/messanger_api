import redis.asyncio as redis # type: ignore
from app.settings import settings


client = redis.Redis(protocol=3).from_url(str(settings.redis_url(0)))



async def get_redis() -> redis.Redis:
    return client
