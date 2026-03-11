from fastapi import FastAPI
from app.database import Base, engine
from app.routes import auth_routes, chat_routes

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Chat System with Gemini")

# Include routers
app.include_router(auth_routes.router)
app.include_router(chat_routes.router)