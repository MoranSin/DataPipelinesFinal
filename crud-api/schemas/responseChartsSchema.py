from pydantic import BaseModel
from typing import List, Dict
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

    def __hash__(self):
        return hash((self.position, self.song, self.artist, self.duration, self.spotify_url))

    def __eq__(self, other):
        if isinstance(other, ChartEntry):
            return (self.position, self.song, self.artist, self.duration, self.spotify_url) == (other.position, other.song, other.artist, other.duration, other.spotify_url)
        return False

class ChartResponse(BaseModel):
    date: date
    source: Dict[str, List[ChartEntry]]