from pydantic import BaseModel, validator
from uuid import UUID, uuid4

class Genre(BaseModel):
    genre_id: UUID
    genre_name: str

    class Config:
        from_attributes = True

class GenreCreate(BaseModel):
    genre_name: str

    @validator("genre_name")
    def genre_name_must_not_be_empty(cls, v: str) -> str:
        if v == "":
            raise ValueError("Genre name must not be empty")
        return v