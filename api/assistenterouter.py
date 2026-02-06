from fastapi import APIRouter, Depends
from service.queryservice import query_simples
from service.assistenteservice import assistente_question
from db.database import get_db
from db.models import User, ChatMessage
from sqlalchemy.orm import Session
from api.authenticationrouter import get_current_user

router = APIRouter()

@router.post('/api/assistente/query', summary='pesquisa o BD e retorna uma mensagem inteligente.')
async def assistente_query(search: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    response_dbvectorextract = query_simples(search=search)

    response = assistente_question(question=search, shortextract=response_dbvectorextract)
    
    # Save Chat History
    # Extract content safely
    answer_text = "Desculpe, não consegui gerar uma resposta."
    
    if isinstance(response, dict) and 'error' in response:
        answer_text = f"Erro no serviço de IA: {response['error']}"
    elif hasattr(response, 'content'):
        answer_text = response.content
    elif isinstance(response, dict) and 'content' in response:
        answer_text = response['content']
    else:
        answer_text = str(response)

    # Save Chat History
    try:
        new_msg = ChatMessage(
            usuario=user.username,
            tenant_id=user.tenant_id,
            pergunta=search,
            resposta=answer_text,
            feedback=0
        )
        db.add(new_msg)
        db.commit()
    except Exception as e:
        print(f"Error saving chat history: {e}")
    
    return {"answer": answer_text}