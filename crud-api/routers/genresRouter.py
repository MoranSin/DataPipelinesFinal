from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.genresSchema import GenreCreate, Genre
from services.genresService import fetch_genres, fetch_genre_by_id, create_genre, fetch_genre_by_name
from config.database import get_db
from uuid import UUID

genresRouter = APIRouter()

@genresRouter.get("/genres", response_model=list[Genre])
async def get_genres(db: Session = Depends(get_db)):
    """Retrieve all genres."""
    genres = fetch_genres(db)
    if genres is None:
        raise HTTPException(status_code=404, detail="Genres not found")
    return genres

@genresRouter.get("/genres/{genre_id}", response_model=Genre)
async def get_genre_by_id(genre_id: UUID, db: Session = Depends(get_db)):
    """Retrieve genre by ID."""
    genre = fetch_genre_by_id(db, genre_id)
    if genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    return genre

@genresRouter.get("/genres/name/{genre_name}", response_model=Genre)
async def get_genre_by_name(genre_name: str, db: Session = Depends(get_db)):
    """Retrieve genre by name."""
    genre = fetch_genre_by_name(db, genre_name)
    if genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    return genre

@genresRouter.post("/genres", response_model=Genre)
async def post_genre(genre: GenreCreate, db: Session = Depends(get_db)):
    """Create a new genre and return it."""
    new_genre = create_genre(db, genre)
    return new_genre
