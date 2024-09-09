from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from routers.songsRouter import songsRouter
from routers.genresRouter import genresRouter
from routers.artistsRouter import artistsRouter
from routers.chartsRouter import chartsRouter

from config.database import test_connection, create_db

"""
FastAPI Application Setup

This script initializes a FastAPI application with the following features:
1. **CORS Middleware**: Configured to allow requests from any origin, supporting cross-origin resource sharing (CORS).
2. **Database Connection**: On application startup, it tests the database connection and creates the database if needed.
3. **API Endpoints**: Includes routers for managing different API routes:
4. **Lambda Compatibility**: Uses the Mangum adapter to enable the FastAPI app to run on AWS Lambda.

"""

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
