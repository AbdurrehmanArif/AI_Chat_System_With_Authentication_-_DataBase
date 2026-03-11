from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app import models, schemas, services, auth
from app.database import get_db
from app.core.config import settings

router = APIRouter(tags=["chat"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("user_id")
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/chat", response_model=schemas.ChatResponse)
def chat_endpoint(request: schemas.ChatRequest, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    
    ai_reply = services.llm_service.get_gemini_response(request.prompt)

    chat = models.ChatMessage(user_id=user.id, prompt=request.prompt, response=ai_reply)
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return {"reply": ai_reply}

@router.get("/history", response_model=list[schemas.ChatHistory])
def get_history(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    chats = db.query(models.ChatMessage).filter(models.ChatMessage.user_id == user.id).order_by(models.ChatMessage.created_at).all()
    return chats