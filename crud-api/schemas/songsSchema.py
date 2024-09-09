from pydantic import BaseModel, validator
from uuid import UUID, uuid4
from typing import Any
import re

class Song(BaseModel):
    """Model for a song with all attributes."""
    song_id: UUID
    artist_id: UUID
    genre_id: UUID
    song_name: str
    song_link: str
    song_lyrics: str
    song_length: str
    song_language: str

    class Config:
        """Configuration to enable attribute-based instantiation."""
        from_attributes = True

class SongCreate(BaseModel):
    """Model for creating a song."""
    artist_id: UUID
    genre_id: UUID
    song_name: str
    song_link: str
    song_lyrics: str
    song_length: str
    song_language: str

    @validator("song_name")
    def song_name_must_not_be_empty(cls, v: str) -> str:
        """Ensure song name is not empty."""
        if v == "":
            raise ValueError("Song name must not be empty")
        return v
    
    @validator("song_length")
    def song_length_must_be_in_correct_format(cls, v: str) -> str:
        """Validate song length format as MM:SS."""
        if not re.match(r'^\d{1,2}:\d{2}$', v):
            raise ValueError("Song length must be in the format MM:SS")
        return v

    