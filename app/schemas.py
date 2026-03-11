from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class ChatRequest(BaseModel):
    prompt: str

class ChatResponse(BaseModel):
    reply: str

class ChatHistory(BaseModel):
    prompt: str
    response: str
    created_at: datetime