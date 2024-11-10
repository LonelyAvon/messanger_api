

from datetime import datetime, timedelta, timezone
from app.settings import settings
from app.api.schemas.news import News
from app.api.utils.async_connector import AsyncHttpClient


class NewsService:
    def __init__(self, client: AsyncHttpClient):
        self.client = client


    async def get_news_feed(self) -> News:
        params = {
        "apiKey": settings.NEWS_TOKEN,
        # "country": "ru",
        "language": "ru",
        "start_date": str(datetime.now(timezone.utc) - timedelta(days=10))
    }
        response = await self.client.get("/search", params=params)
        return News(**response)
