from jose import JWTError, jwt
from passlib.context import CryptContext
import os
from fastapi import HTTPException, status
from datetime import datetime, timedelta


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    secret_key = os.getenv("JWT_SECRET", "default_secret")
    algorithm = "HS256"
    print("mine",secret_key)
    # Get expiration time from environment variable and convert to integer
    expire_minutes = int(os.getenv("JWT_EXPIRE", 30))  # Default to 30 minutes if not set
    expire = datetime.utcnow() + timedelta(minutes=expire_minutes)
    to_encode.update({"exp": expire})  # Add expiration to the token payload
    
    return jwt.encode(to_encode, secret_key, algorithm=algorithm)

def decode_token(token: str) -> dict:
    secret_key = os.getenv("JWT_SECRET", "default_secret")
    algorithm = "HS256"
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")  # Raise an exception on error