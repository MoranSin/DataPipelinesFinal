from pydantic import BaseModel, validator
from uuid import UUID, uuid4
from datetime import date

class Chart(BaseModel):
    rank_id: UUID
    artist_id: UUID
    song_id: UUID
    rank_value : int
    date : date
    source : str
    country_code : str
    chart_type : str

    class Config:
        from_attributes = True

class ChartCreate(BaseModel):
    artist_id: UUID
    song_id: UUID
    rank_value : int
    date : date
    source : str
    country_code : str
    chart_type : str
