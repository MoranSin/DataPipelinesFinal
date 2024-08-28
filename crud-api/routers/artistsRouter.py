from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from schemas.artistsSchema import ArtistCreate, Artist
from services.artistsService import fetch_artists, fetch_artist_by_id, create_artist, update_artist, fetch_artist_by_name
from config.database import get_db
from uuid import UUID

artistsRouter = APIRouter()

@artistsRouter.get("/artists", response_model=list[Artist])
async def get_artists(db: Session = Depends(get_db)):
    artists = fetch_artists(db)
    if artists is None:
        raise HTTPException(status_code=404, detail="Artists not found")
    return artists

@artistsRouter.get("/artists/{artist_id}", response_model=Artist)
async def get_artist_by_id(artist_id: UUID, db: Session = Depends(get_db)):
    artist = fetch_artist_by_id(db, artist_id)
    if artist is None:
        raise HTTPException(status_code=404, detail="Artist not found")
    return artist

@artistsRouter.post("/artists", response_model=Artist)
async def post_artist(artist: ArtistCreate, db: Session = Depends(get_db)):
    new_artist = create_artist(db, artist)
    return new_artist

@artistsRouter.patch("/artists/{artist_id}", response_model=Artist)
async def patch_artist(artist_id: UUID, artist: ArtistCreate, db: Session = Depends(get_db)):
    updated_artist = update_artist(db, artist_id, artist)
    return updated_artist

@artistsRouter.get("/artists/name/{artist_name}", response_model=Artist)
async def get_artist_by_name(artist_name: str, db: Session = Depends(get_db)):
    artist = fetch_artist_by_name(db, artist_name)
    if artist is None:
        raise HTTPException(status_code=404, detail="Artist not found")
    return artist