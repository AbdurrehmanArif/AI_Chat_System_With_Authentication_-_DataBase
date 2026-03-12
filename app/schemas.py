from pydantic import BaseModel

class SignupSchema(BaseModel):
    name: str
    email: str
    password: str


class LoginSchema(BaseModel):
    email: str
    password: str


class ChatRequest(BaseModel):
    prompt: str


class ChatResponse(BaseModel):
    reply: str
