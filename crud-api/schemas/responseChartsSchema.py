from pydantic import BaseModel
from typing import List, Dict
from datetime import date

class SongFeatures(BaseModel):
    """Model for song features like genre and language."""
    genre: str
    language: str

class ArtistFeatures(BaseModel):
    """Model for artist features like gender and type."""
    gender: str
    type: str

class ChartEntry(BaseModel):
    """Model for an entry in a chart with song and artist details."""
    position: int
    song: str
    artist: str
    duration: str
    spotify_url: str
    source: str
    songFeatures: SongFeatures
    artistFeatures: ArtistFeatures

    def __hash__(self):
        """Hash function based on key attributes."""
        return hash((self.position, self.song, self.artist, self.duration, self.spotify_url, self.source))

    def __eq__(self, other):
        """Check equality based on key attributes."""
        if isinstance(other, ChartEntry):
            return (self.position, self.song, self.artist, self.duration, self.spotify_url, self.source) == (other.position, other.song, other.artist, other.duration, other.spotify_url, other.source)
        return False

class ChartResponse(BaseModel):
    """Model for chart response with date and a dictionary of charts."""
    date: date
    charts: Dict[str, List[ChartEntry]]
