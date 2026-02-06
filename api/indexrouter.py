from fastapi import APIRouter
from service.indexservice import create_index, list_index, detail_index

router = APIRouter()

@router.post('/api/index/create', summary='create index from pinecone')
async def create_index_router(name_index : str):
    response = create_index(name_index)
    return {f"the index {response}"}

@router.get('/api/index/list', summary='list index from pinecone')
async def list_index_router():
    response = list_index()
    return response

@router.post('/api/index/detail', summary='detail index from pinecone')
async def detail_index_router(name_index:str):
    response = detail_index(name_index)
    return response
