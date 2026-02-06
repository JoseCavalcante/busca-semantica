from fastapi import APIRouter, File, UploadFile
from service.extracaoPDFservice import extract_text_from_pdf, split_text_into_chunks
from service.embeddingservice import embeddingService

router = APIRouter()

@router.post('/api/extracaoPDF/pdf', summary='Extract text from pdf')
async def pdf_to_text(filePDF:UploadFile=File(...)):
    response = extract_text_from_pdf(filePDF)
    return response

@router.post('/api/extracaoPDF/split_text_in_chunks_simples', summary='split text into chunk')
async def split_text_in_chunks_simples(text:str):
    response = split_text_into_chunks(text=text)
    return response

@router.post('/api/extracaoPDF/split_text_in_chunks_embeddings', summary='split text into chunk and create a list of embeddings')
async def split_text_in_chunks_embeddings(text:str):

    chunks_list = split_text_into_chunks(text=text)
    
    try:
        embeddings = []

        for chunk in chunks_list:
            embeddings.append(embeddingService(chunk=chunk))

        return embeddings
    except Exception as e:
        return {"error":str(e)}
