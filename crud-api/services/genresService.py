from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from models.genreModel import Genre
from schemas.genresSchema import GenreCreate
from uuid import uuid4
import logging

logging.basicConfig(level=logging.INFO)

def fetch_genres(db: Session):
    """Retrieve all genres."""
    try:    
        return db.query(Genre).all()
    except NoResultFound:
        return None

def fetch_genre_by_id(db: Session, genre_id: uuid4):
    """Retrieve genre by ID."""
    try:
        return db.query(Genre).filter(Genre.genre_id == genre_id).first()
    except NoResultFound:
        return None
    
def create_genre(db: Session, genre: GenreCreate):
    """Create a new genre and return it."""
    try:
        new_genre = Genre(
            genre_id = uuid4(),
            genre_name = genre.genre_name
        )
        db.add(new_genre)
        db.commit()
        db.refresh(new_genre)
        return new_genre
    except Exception as e:
        logging.error(f"Failed to create genre: {e}")
        return None

def fetch_genre_by_name(db: Session, genre_name: str):
    """Retrieve genre by name."""
    try:
        return db.query(Genre).filter(Genre.genre_name == genre_name).first()
    except NoResultFound:
        return None
    
