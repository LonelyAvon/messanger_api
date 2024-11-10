from datetime import datetime
import re
from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl, field_validator, field_serializer

from typing_extensions import Annotated

class NewsPost(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    url: Optional[str] = None  # Для URL
    author: Optional[str] = None
    image: Optional[str] = None  # Для изображения
    category: Optional[List[str]] = None
    published: Optional[datetime] = None  # Ожидаем datetime без временной зоны

    @field_validator('published', mode='before')
    def parse_published(cls, value):
        if value is None:
            return None
        try:
            # Убираем временную зону, если она есть
            return datetime.fromisoformat(value).replace(tzinfo=None)
        except ValueError:
            raise ValueError('Invalid datetime format, expected YYYY-MM-DD HH:MM:SS')


class News(BaseModel):
    status: str
    news: List[NewsPost]