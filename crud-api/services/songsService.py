from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from sqlalchemy.sql import text
from models.songsModel import Song
from schemas.songsSchema import SongCreate
from uuid import uuid4
import logging

logging.basicConfig(level=logging.INFO)

def fetch_songs(db: Session):
    return db.query(Song).all()

def fetch_song_by_id(db: Session, song_id: uuid4):
    try:
        return db.query(Song).filter(Song.song_id == song_id).first()
    except NoResultFound:
        return None

def create_song(db: Session, song: SongCreate):

    new_song = Song(
        song_id = uuid4(),
        artist_id = song.artist_id,
        genre_id = song.genre_id,
        song_name = song.song_name,
        song_link = song.song_link,
        song_lyrics = song.song_lyrics,
        song_length = song.song_length
    )
    db.add(new_song)
    db.commit()
    db.refresh(new_song)
    return new_song

def update_song(db: Session, song_id: uuid4, song: SongCreate):
    db_song = db.query(Song).filter(Song.song_id == song_id).first()
    db_song.artist_id = song.artist_id
    db_song.genre_id = song.genre_id
    db_song.song_name = song.song_name
    db_song.song_link = song.song_link
    db_song.song_lyrics = song.song_lyrics
    db_song.song_length = song.song_length
    db.commit()
    db.refresh(db_song)
    return db_song

def fetch_song_by_name(db: Session, song_name: str):
    try:
        return db.query(Song).filter(Song.song_name == song_name).first()
    except NoResultFound:
        return None