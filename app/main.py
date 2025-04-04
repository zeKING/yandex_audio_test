from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.users.router import router as router_user
from app.audio.router import router as router_audio

app = FastAPI()

app.include_router(router_user)
app.include_router(router_audio)

app.mount('/media', StaticFiles(directory='media'), name='media')

origins = [
    "http:localhost:5173",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

