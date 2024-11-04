import redis.asyncio as redis # type: ignore
from app.settings import settings





async def get_redis():
    client = redis.Redis(protocol=3).from_url(str(settings.redis_url(0)))
    try:
        yield client
    finally:
        await client.close()