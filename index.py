from fastapi import FastAPI
from routes.note import note

server = FastAPI()

server.include_router(note)