from sqlalchemy import Column, String, ForeignKey, Integer, Date
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from pydantic import BaseModel, RootModel
from typing import Dict, List

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
    chart_type = Column(String, nullable=False)


class DayList(RootModel[List[str]]):
    pass

class MonthDict(RootModel[Dict[str, DayList]]):
    pass

class YearDict(RootModel[Dict[str, MonthDict]]):
    pass
