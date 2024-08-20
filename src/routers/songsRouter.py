from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from schemas.songsSchema import SongCreate, Song
from services.songsService import get_songs, get_song_by_id, create_song, update_song
from config.database import get_db, test_connection, create_db

test_connection()
create_db()

songsRouter = APIRouter()

@songsRouter.get("/songs", response_model=list[Song])
async def get_songs(db: Session = Depends(get_db)):
    songs = get_songs(db)
    return songs

@songsRouter.get("/songs/{song_id}", response_model=Song)
async def get_song_by_id(song_id: int, db: Session = Depends(get_db)):
    song = get_song_by_id(db, song_id)
    if song is None:
        raise HTTPException(status_code=404, detail="Song not found")
    return song

@songsRouter.post("/songs", response_model=Song)
async def create_song(song: SongCreate, db: Session = Depends(get_db)):
    user = create_song(db, song)
    return user

@songsRouter.patch("/songs/{song_id}", response_model=Song)
async def update_song(song_id: int, song: SongCreate, db: Session = Depends(get_db)):
    user = update_song(db, song_id, song)
    return user

