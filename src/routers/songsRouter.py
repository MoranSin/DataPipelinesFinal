from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from schemas.songsSchema import SongCreate, Song
from services.songsService import fetch_songs, fetch_song_by_id, create_song, update_song
from config.database import get_db
from uuid import UUID

songsRouter = APIRouter()

@songsRouter.get("/songs", response_model=list[Song])
async def get_songs(db: Session = Depends(get_db)):
    songs = fetch_songs(db)
    if songs is None:
        raise HTTPException(status_code=404, detail="Songs not found")
    return songs

@songsRouter.get("/songs/{song_id}", response_model=Song)
async def get_song_by_id(song_id: UUID, db: Session = Depends(get_db)):
    song = fetch_song_by_id(db, song_id)
    if song is None:
        raise HTTPException(status_code=404, detail="Song not found")
    return song

@songsRouter.post("/songs", response_model=Song)
async def post_song(song: SongCreate, db: Session = Depends(get_db)):
    user = create_song(db, song)
    return user

@songsRouter.patch("/songs/{song_id}", response_model=Song)
async def patch_song(song_id: UUID, song: SongCreate, db: Session = Depends(get_db)):
    user = update_song(db, song_id, song)
    return user

