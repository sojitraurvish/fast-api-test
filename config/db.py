from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

print("check", os.getenv("MONGO_URI"), "mine")  # This should now print the correct URI

client = MongoClient(os.getenv("MONGO_URI"))
db = client.get_database("pytest")  # Replace with your actual database name

# Ensure the 'users' collection is accessible
users_collection = db["users"]  # Replace with your actual collection name
print(users_collection)
