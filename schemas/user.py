from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

class User(BaseModel):
    email: str
    password: str

class UserUpdate(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class UserWithMessageResponse(BaseModel):
    messages: str
    user: UserResponse
    model_config = ConfigDict(from_attributes=True)
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str