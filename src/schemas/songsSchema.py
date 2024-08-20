from pydantic import BaseModel, validator
from uuid import UUID, uuid4
from typing import Any

class Song(BaseModel):
    song_id: UUID
    artist_id: UUID
    genre_id: UUID
    song_name: str
    song_link: str
    song_lyrics: str
    song_length: int

    class Config:
        from_attributes = True

class SongCreate(BaseModel):
    artist_id: UUID
    genre_id: UUID
    song_name: str
    song_link: str
    song_lyrics: str
    song_length: int

    # @validator("song_name")
    # def song_name_must_not_be_empty(cls, v: str) -> str:
    #     if v == "":
    #         raise ValueError("Song name must not be empty")
    #     return v

    # @validator("song_link")
    # def song_link_must_not_be_empty(cls, v: str) -> str:
    #     if v == "":
    #         raise ValueError("Song link must not be empty")
    #     return v

    # @validator("song_lyrics")
    # def song_lyrics_must_not_be_empty(cls, v: str) -> str:
    #     if v == "":
    #         raise ValueError("Song lyrics must not be empty")
    #     return v

    # @validator("song_length")
    # def song_length_must_be_positive(cls, v: int) -> int:
    #     if v <= 0:
    #         raise ValueError("Song length must be positive")
    #     return v
    