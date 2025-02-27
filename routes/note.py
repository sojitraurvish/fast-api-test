from fastapi import APIRouter
from models.note import Note
from config.db import conn
from schemas.note import noteEntity,notesEntity

note = APIRouter()

@note.get("/")
def read_root():
    docs= conn.pytest.users.find_one({})
    print(docs)
    return {"Hello": "World mine"}

@note.post("/")
def add_note(note:Note):
    inserted_note = conn.pytest.users.insert_one(dict(note))
    return noteEntity(inserted_note)