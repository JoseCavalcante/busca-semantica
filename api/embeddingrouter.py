from service.embeddingservice import embeddingService
from fastapi import APIRouter

router = APIRouter()

@router.post('/api/embeding', summary='create embeding from openAI')
async def embedding_router(chunk : str):
    response = embeddingService(chunk=chunk)
    return response