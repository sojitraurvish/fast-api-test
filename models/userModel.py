from pydantic import BaseModel, EmailStr

class User(BaseModel):
    name: str
    email: EmailStr
    password: str
    pic: str = "https://icon-library.com/images/anonymous-avatar-icon/anonymous-avatar-icon-25.jpg"