from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from routers.songsRouter import songsRouter 
from routers.genresRouter import genresRouter
from routers.artistsRouter import artistsRouter
from routers.chartsRouter import chartsRouter

from config.database import test_connection, create_db

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    test_connection()
    create_db()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Skibidi API"}
    
app.include_router(chartsRouter)
app.include_router(songsRouter)
app.include_router(artistsRouter)
app.include_router(genresRouter)

handler = Mangum(app)