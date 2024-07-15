from sqlalchemy.orm import DeclarativeBase

from app.db.metadata import meta


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta
