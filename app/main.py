from fastapi import FastAPI, Response, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, List
from random import randrange
from .import models, schemas, utils
from .database import engine, get_db
from . routers import posts, users, auth, vote
from .config import Settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware



origins = [
    "https://www.google.com",
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8000",
    "https://www.youtube.com"
]
# origins = ["*"]   # For Taking Every Domain....

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")    
def read_root():
    return {"Hello": "World"}

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)
