from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

from config.database import Base 

class Song(Base):
    __tablename__ = "songs"

    song_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    artist_id = Column(UUID(as_uuid=True), ForeignKey("artists.artist_id"), nullable=False)
    genre_id = Column(UUID(as_uuid=True), ForeignKey("genres.genre_id"), nullable=False)
    song_name = Column(String, unique=True, nullable=False)
    song_link = Column(String, nullable=False)
    song_lyrics = Column(String, nullable=False)
    song_length = Column(String, nullable=False)
