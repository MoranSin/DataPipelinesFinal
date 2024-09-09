from pydantic import BaseModel, validator
from uuid import UUID
class Genre(BaseModel):
    """Model for a genre with ID and name."""
    genre_id: UUID
    genre_name: str

    class Config:
        """Configuration to enable attribute-based instantiation."""
        from_attributes = True

class GenreCreate(BaseModel):
    """Model for creating a genre."""
    genre_name: str

    @validator("genre_name")
    def genre_name_must_not_be_empty(cls, v: str) -> str:
        """Ensure genre name is not empty."""
        if v == "":
            raise ValueError("Genre name must not be empty")
        return v