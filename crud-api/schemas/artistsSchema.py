from pydantic import BaseModel, validator
from uuid import UUID, uuid4

class Artist(BaseModel):
    """Model for an artist with required attributes."""
    artist_id: UUID
    artist_name: str
    genre_id: UUID
    country_code: str
    artist_gender: str

    class Config:
        """Configuration to enable attribute-based instantiation."""
        from_attributes = True

class ArtistCreate(BaseModel):
    """Model for creating an artist."""
    artist_name: str
    genre_id: UUID
    country_code: str
    artist_gender: str

    @validator("artist_name")
    def artist_name_must_not_be_empty(cls, v: str) -> str:
        """Validate that the artist name is not empty."""
        if v == "":
            raise ValueError("Artist name must not be empty")
        return v
    