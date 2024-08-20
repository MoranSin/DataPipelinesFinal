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

@songsRouter.get("/songs/{song_id}")
async def get_song_by_id(song_id: int):
    return {"name": "song1"}

@songsRouter.post("/songs")
async def create_song():
    return {"name": "song1"}

@songsRouter.patch("/songs/{song_id}")
async def update_song(song_id: int):
    return {"name": "song1"}

