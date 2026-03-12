from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import ChatRequest
from app.auth import get_current_user
from app import models
from app.services.llm_service import generate_reply

router = APIRouter()


@router.post("/chat")
def chat(
    request: ChatRequest,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    reply = generate_reply(request.prompt)

    chat = models.ChatMessage(
        user_id=user_id,
        prompt=request.prompt,
        response=reply
    )

    db.add(chat)
    db.commit()

    return {"reply": reply}


@router.get("/history")
def get_history(
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    chats = db.query(models.ChatMessage).filter(
        models.ChatMessage.user_id == user_id
    ).all()

    return chats
