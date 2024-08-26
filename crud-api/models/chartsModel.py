from sqlalchemy import Column, String, ForeignKey, Integer, Date
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

from config.database import Base 

class Chart(Base):
    __tablename__ = "charts"

    rank_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    artist_id = Column(UUID(as_uuid=True), ForeignKey("artists.artist_id"), nullable=False)
    song_id = Column(UUID(as_uuid=True), ForeignKey("songs.song_id"), nullable=False)
    rank_value = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    source = Column(String, nullable=False)
    country_code = Column(String, nullable=False)