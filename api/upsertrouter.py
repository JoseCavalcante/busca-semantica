from fastapi import APIRouter, File, UploadFile, Form
from service.extracaoPDFservice import extract_text_from_pdf, extract_pdf_metadata, split_text_into_chunks
from  api.extracaoPDFrouter import split_text_in_chunks_embeddings, split_text_in_chunks_simples
from service.upsertservice import upsertService, upsertService_Metadados, upsert_rich_vectors
from service.embeddingservice import embeddingService
import json
import uuid

router = APIRouter()

@router.post('/api/upsert/pdf', summary='Upsert a document PDF into database')
async def upsert(filePDF:UploadFile=File(...)):
    # 1. Extract Rich Data
    pdf_data = extract_pdf_metadata(filePDF)
    
    global_meta = pdf_data["metadata"]
    pages = pdf_data["content"]
    
    vectors_to_upsert = []

    # 2. Process each page
    for page in pages:
        page_text = page["text"]
        page_num = page["page_number"]
        page_stats = page["stats"]
        page_entities = page["entities"]
        
        # Split page text into chunks
        chunks = split_text_into_chunks(page_text)
        
        for i, chunk in enumerate(chunks):
            # Generate Embedding
            embedding = embeddingService(chunk)
            
            # Combine all metadata
            # Flattening some structure for Pinecone query compatibility
            chunk_metadata = {
                # Global
                "filename": global_meta["filename"],
                "author": global_meta["author"],
                "creation_date": global_meta["creation_date"],
                "total_pages": global_meta["page_count"],
                
                # Page/Chunk Specific
                "page_number": page_num,
                "chunk_index": i,
                "text": chunk, # The chunk text itself
                "chunk_char_count": len(chunk),
                
                # Entities (Found on this page)
                "page_emails": page_entities["emails"],
                "page_phones": page_entities["phones"],
                "page_links": page_entities["links"]
            }
            
            # Create valid vector object
            vectors_to_upsert.append({
                "id": str(uuid.uuid4()),
                "values": embedding,
                "metadata": chunk_metadata
            })

    # 3. Upsert
    if not vectors_to_upsert:
        return {"message": "No text content found in PDF to upsert."}
        
    response = upsert_rich_vectors(vectors_to_upsert)

    return response

@router.post('/api/upsert/pdf_metadados', summary='Upsert a document PDF into database with metadados')
async def upsert_metadata(filePDF:UploadFile=File(...), metadata: str = Form(...)):
    try:
        metadataJson = json.loads(metadata)

        textfrompdf = extract_text_from_pdf(filePDF)
        chuncklistText = await split_text_in_chunks_simples(text=textfrompdf)
        response = upsertService_Metadados(metadata=metadataJson, chuncklisttext=chuncklistText)
    
        return {"message": f"Sucesso inserido {response} registros."}
    except Exception as e:
        return {"error": str(e)}

