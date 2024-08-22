from fastapi import FastAPI
from mangum import Mangum
from routers.songsRouter import songsRouter 
from routers.genresRouter import genresRouter
from routers.artistsRouter import artistsRouter

import uvicorn
from config.database import test_connection, create_db

app = FastAPI()

@app.on_event("startup")
async def startup():
    test_connection()
    create_db()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Skibidi API"}
    
app.include_router(songsRouter)
app.include_router(artistsRouter)
app.include_router(genresRouter)


handler = Mangum(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)