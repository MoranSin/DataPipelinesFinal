from fastapi import FastAPI
from mangum import Mangum
from routers.songsRouter import songsRouter 
import uvicorn

app = FastAPI()
app.include_router(songsRouter)
handler = Mangum(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)