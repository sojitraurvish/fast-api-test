from typing import Union

from fastapi import FastAPI
from pymongo import MongoClient

server = FastAPI()

conn = MongoClient("mongodb+srv://urvish:adminurvish@cluster0.uobkf.mongodb.net/pytest")

@server.get("/")
def read_root():
    docs= conn.pytest.users.find_one({})
    print(docs)
    return {"Hello": "World mine"}


@server.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
