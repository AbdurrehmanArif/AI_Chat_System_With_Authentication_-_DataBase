from fastapi import FastAPI

from app.database import engine
from app import models

from app.routes import auth_routes, chat_routes

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_routes.router)
app.include_router(chat_routes.router)
