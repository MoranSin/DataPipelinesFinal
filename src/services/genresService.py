from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from models.genreModel import Genre
from schemas.genresSchema import GenreCreate
from uuid import uuid4
import logging

logging.basicConfig(level=logging.INFO)

def fetch_genres(db: Session):
    return db.query(Genre).all()

def fetch_genre_by_id(db: Session, genre_id: uuid4):
    try:
        return db.query(Genre).filter(Genre.genre_id == genre_id).first()
    except NoResultFound:
        return None
    
def create_genre(db: Session, genre: GenreCreate):
    new_genre = Genre(
        genre_id = uuid4(),
        genre_name = genre.genre_name
    )
    db.add(new_genre)
    db.commit()
    db.refresh(new_genre)
    return new_genre