from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

from config.database import Base 

class Genre(Base):
    """SQLAlchemy model for the 'genres' table."""
    __tablename__ = "genres"

    genre_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    genre_name = Column(String, unique=True, nullable=False)