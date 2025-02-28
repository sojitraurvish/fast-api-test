from fastapi import FastAPI
from routes import auth
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Print to verify that the environment variables are loaded
print("Mongo URI:", os.getenv("MONGO_URI"))
print("JWT Secret:", os.getenv("JWT_SECRET"))

app = FastAPI()

app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "API is Running..."}