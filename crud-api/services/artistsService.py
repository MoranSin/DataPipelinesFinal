from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from models.artistsModel import Artist
from schemas.artistsSchema import ArtistCreate
from uuid import uuid4
import logging

logging.basicConfig(level=logging.INFO)

def fetch_artists(db: Session):
    return db.query(Artist).all()

def fetch_artist_by_id(db: Session, artist_id: uuid4):
    try:
        return db.query(Artist).filter(Artist.artist_id == artist_id).first()
    except NoResultFound:
        return None
    
def create_artist(db: Session, artist: ArtistCreate):
    try:
        new_artist = Artist(
            artist_id = uuid4(),
            artist_name = artist.artist_name,
            genre_id = artist.genre_id,
            country_code = artist.country_code,
            artist_gender = artist.artist_gender
        )
        db.add(new_artist)
        db.commit()
        db.refresh(new_artist)
        return new_artist
    except Exception as e:
        logging.error(f"Failed to create artist: {e}")
        return None

def update_artist(db: Session, artist_id: uuid4, artist: ArtistCreate):
    try:
        db_artist = db.query(Artist).filter(Artist.artist_id == artist_id).first()
        db_artist.artist_name = artist.artist_name
        db_artist.genre_id = artist.genre_id
        db_artist.country_code = artist.country_code
        db_artist.artist_gender = artist.artist_gender
        db.commit()
        db.refresh(db_artist)
        return db_artist
    except Exception as e:
        logging.error(f"Failed to update artist: {e}")
        return None

def fetch_artist_by_name(db: Session, artist_name: str):
    try:
        return db.query(Artist).filter(Artist.artist_name == artist_name).first()
    except NoResultFound:
        return None


