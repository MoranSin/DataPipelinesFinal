from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from sqlalchemy.sql import text
from models.songsModel import Song
from schemas.songsSchema import SongCreate
from uuid import uuid4
import logging

logging.basicConfig(level=logging.INFO)

def fetch_songs(db: Session):
    """Fetches all songs from the database."""
    try:
        return db.query(Song).all()
    except NoResultFound:
        return None

def fetch_song_by_id(db: Session, song_id: uuid4):
    """Fetches a song from the database by its ID."""
    try:
        return db.query(Song).filter(Song.song_id == song_id).first()
    except NoResultFound:
        return None

def create_song(db: Session, song: SongCreate):
    """Creates a new song in the database."""
    try:
        new_song = Song(
            song_id = uuid4(),
            artist_id = song.artist_id,
            genre_id = song.genre_id,
            song_name = song.song_name,
            song_link = song.song_link,
            song_lyrics = song.song_lyrics,
            song_length = song.song_length,
            song_language = song.song_language
        )
        db.add(new_song)
        db.commit()
        db.refresh(new_song)
        return new_song
    except Exception as e:
        logging.error(f"Failed to create song: {e}")
        return None  

def update_song(db: Session, song_id: uuid4, song: SongCreate):
    """Updates an existing song in the database."""
    try:
        db_song = db.query(Song).filter(Song.song_id == song_id).first()
        db_song.artist_id = song.artist_id
        db_song.genre_id = song.genre_id
        db_song.song_name = song.song_name
        db_song.song_link = song.song_link
        db_song.song_lyrics = song.song_lyrics
        db_song.song_length = song.song_length
        db_song.song_language = song.song_language
        db.commit()
        db.refresh(db_song)
        return db_song
    except Exception as e:
        logging.error(f"Failed to update song: {e}")
        return None

def fetch_song_by_name(db: Session, song_name: str):
    """Fetches a song from the database by its name."""
    try:
        return db.query(Song).filter(Song.song_name == song_name).first()
    except NoResultFound:
        return None
    
def fetch_song_by_name_and_artist_id(db: Session, song_name: str, artist_id: str):
    """Fetches a song from the database by its name and artist ID."""
    try:
        return db.query(Song).filter(Song.song_name == song_name, Song.artist_id == artist_id).first()
    except NoResultFound:
        return None
