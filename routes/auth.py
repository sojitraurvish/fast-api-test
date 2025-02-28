import sys
import os
import re
import logging
from fastapi import APIRouter, HTTPException, Depends, Body, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr, constr, validator
from models.userModel import User
from utils.auth import get_password_hash, verify_password, create_access_token
from config.db import users_collection
from utils.auth import decode_token 
from bson import ObjectId  # Import ObjectId

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
router = APIRouter()

# Set up logging
logging.basicConfig(level=logging.INFO)

# Define a regex pattern for validating names
NAME_REGEX = r"^[A-Za-z\s]+$"  # Only letters and spaces allowed

# Define a regex pattern for validating passwords
PASSWORD_REGEX = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"  # At least 8 characters, 1 letter, 1 number

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    @validator('password')
    def validate_password(cls, value):
        if not re.match(PASSWORD_REGEX, value):
            raise ValueError('Password must meet the criteria')
        return value

class RegisterRequest(BaseModel):
    name: str  # Change to a simple string type
    email: EmailStr
    password: str

    @validator('name')
    def validate_name(cls, value):
        if not re.match(NAME_REGEX, value):
            raise ValueError('Name must only contain letters and spaces')
        return value

    @validator('password')
    def validate_password(cls, value):
        if not re.match(PASSWORD_REGEX, value):
            raise ValueError('Password must meet the criteria')
        return value

@router.post("/register")
async def register_user(user: RegisterRequest):
    existing_user = users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    hashed_password = get_password_hash(user.password)
    new_user = {
        "name": user.name,
        "email": user.email,
        "password": hashed_password,
    }
    result = users_collection.insert_one(new_user)  # Store the new user and get the result
    new_user["_id"] = str(result.inserted_id)  # Add the user ID to the new_user dict
    
    logging.info(f"User registered: {new_user}")  # Log the new user information
    
    return {
        "_id": new_user["_id"],
        "name": new_user["name"],
        "email": new_user["email"],
        "token": create_access_token({"sub": new_user["email"], "_id": new_user["_id"]}),  # Include user ID
    }

@router.post("/login")
async def login_user(login_request: LoginRequest):
    logging.info(f"Login attempt for email: {login_request.email}")
    user = users_collection.find_one({"email": login_request.email})
    
    if user and verify_password(login_request.password, user["password"]):
        return {
            "_id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"],
            "isAdmin": user.get("isAdmin", False),
            "token": create_access_token({"sub": user["email"], "_id": str(user["_id"])}),  # Include user ID
        }
    else:
        logging.warning("Invalid login attempt")
        raise HTTPException(status_code=401, detail="Invalid email or password")

@router.get("/profile")
async def get_user_profile(token: str = Depends(oauth2_scheme)):
    # Decode the token to get the user information
    user_info = decode_token(token)  # Implement this function to decode the token and get user info
    
    # Check if '_id' is in user_info
    if "_id" not in user_info:
        raise HTTPException(status_code=401, detail="Invalid token: User ID not found")
    
    # Convert the string ID to ObjectId
    user_id = ObjectId(user_info["_id"])  # Convert to ObjectId

    user = users_collection.find_one({"_id": user_id})  # Retrieve user by ObjectId

    if user:
        return {
            "_id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"],
        }
    else:
        logging.warning(f"User not found for ID: {user_info['_id']}")  # Log if user is not found
        raise HTTPException(status_code=404, detail="User not found")

@router.post("/logout")
async def logout_user(token: str = Depends(oauth2_scheme)):
    # Implement your logout logic here, such as invalidating the token
    return {"message": "User logged out successfully"}
