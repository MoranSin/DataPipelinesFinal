from pydantic import BaseModel, Field, Any
from typing import Optional, List
from uuid import UUID
from datetime import date

class SongFeatures(BaseModel):
    key: Optional[str] = None
    genre: Optional[str] = None
    language: Optional[str] = None

class ArtistFeatures(BaseModel):
    type: Optional[str] = None
    gender: Optional[str]  = None

class ChartEntry(BaseModel):
    position: int
    song: str
    artist: str
    duration: str
    spotify_url: str
    songFeatures: dict[str, Any]
    artistFeatures: dict[str, Any]

class Chart(BaseModel):
    date: date 
    source: str 
    country_code: str
    chart_type: str
    charts: List[ChartEntry] 

class ChartResponse(BaseModel):
    # date: date 
    charts: dict[str, dict[str, List[ChartEntry]]]
