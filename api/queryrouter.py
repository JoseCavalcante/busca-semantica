from fastapi import APIRouter, Depends
from service.queryservice import query_simples, query_filtered
from pydantic import BaseModel
from typing import Optional, Dict, Any
from db.models import User, Prompt
from api.authenticationrouter import get_current_user
from sqlalchemy.orm import Session
from db.database import get_db

router = APIRouter()

class AdvancedQueryRequest(BaseModel):
    search_text: str
    filters: Optional[Dict[str, Any]] = None
    top_k: int = 5

@router.post("/api/query/simples", summary="query the database simples")
async def query(search:str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Save Prompt to History
    try:
        new_prompt = Prompt(
            usuario=user.username,
            tenant_id=user.tenant_id,
            tema="simples",
            prompt=search,
            resposta="", # Populated later if needed or left empty for simple search log
        )
        db.add(new_prompt)
        db.commit()
    except Exception as e:
        print(f"Error saving history: {e}")

    response = await query_simples(search=search, tenant_id=user.tenant_id, db=db)
    return response

@router.post("/api/query/advanced", summary="query with metadata filters")
async def query_advanced(request: AdvancedQueryRequest, user: User = Depends(get_current_user)):
    filters = request.filters or {}
    
    response = await query_filtered(
        search=request.search_text, 
        filters=filters,
        top_k=request.top_k
    )
    return response