from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Dict, Any
from db.database import get_db
from db.models import User, Prompt, ChatMessage
from api.authenticationrouter import get_current_user

router = APIRouter()

@router.get("/api/history/prompts", summary="Get recent search history")
async def get_prompt_history(
    limit: int = 50, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    prompts = db.query(Prompt).filter(
        Prompt.tenant_id == current_user.tenant_id
    ).order_by(desc(Prompt.created_at)).limit(limit).all()
    
    return [
        {
            "id": p.id,
            "usuario": p.usuario,
            "prompt": p.prompt,
            "resposta": p.resposta,
            "feedback": p.feedback,
            "created_at": p.created_at.isoformat()
        } for p in prompts
    ]

@router.get("/api/history/chat", summary="Get recent chat history")
async def get_chat_history(
    limit: int = 50, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    chats = db.query(ChatMessage).filter(
        ChatMessage.tenant_id == current_user.tenant_id
    ).order_by(desc(ChatMessage.created_at)).limit(limit).all()
    
    return [
        {
            "id": c.id,
            "usuario": c.usuario,
            "pergunta": c.pergunta,
            "resposta": c.resposta,
            "feedback": c.feedback,
            "created_at": c.created_at.isoformat()
        } for c in chats
    ]
