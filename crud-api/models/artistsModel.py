from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

from config.database import Base 

class Artist(Base):
    """SQLAlchemy model for the 'artists' table."""
    __tablename__ = "artists"

    artist_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    artist_name = Column(String, nullable=False)
    genre_id = Column(UUID(as_uuid=True), ForeignKey("genres.genre_id"), nullable=False)
    country_code = Column(String, nullable=False)
    artist_gender = Column(String, nullable=False)

