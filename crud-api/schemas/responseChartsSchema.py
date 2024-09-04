from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from datetime import date

class SongFeatures(BaseModel):
    genre: str
    language: str

class ArtistFeatures(BaseModel):
    gender: str

class ChartEntry(BaseModel):
    position: int
    song: str
    artist: str
    duration: str
    spotify_url: str
    songFeatures: SongFeatures
    artistFeatures: ArtistFeatures

class ChartResponse(BaseModel):
    date: date
    charts: Dict[str, List[ChartEntry]]