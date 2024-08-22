from pydantic import BaseModel, validator
from uuid import UUID, uuid4

class Artist(BaseModel):
    artist_id: UUID
    artist_name: str
    genre_id: UUID
    country_code: str
    artist_gender: str

    class Config:
        from_attributes = True

class ArtistCreate(BaseModel):
    artist_name: str
    genre_id: UUID
    country_code: str
    artist_gender: str

    @validator("artist_name")
    def artist_name_must_not_be_empty(cls, v: str) -> str:
        if v == "":
            raise ValueError("Artist name must not be empty")
        return v
    