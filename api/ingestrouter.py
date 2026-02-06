from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Depends
import json
import uuid
from typing import Optional
from db.models import User
from api.authenticationrouter import get_current_user

from service.extracaoPDFservice import extract_pdf_metadata, split_text_into_chunks, extract_docx_metadata
from service.enrichmentservice import enrich_resume_data
from service.embeddingservice import embeddingService
from service.upsertservice import upsert_rich_vectors

router = APIRouter()

@router.post('/api/ingest', summary='Ingest File (PDF/TXT) with full pipeline')
async def ingest_file(
    file: UploadFile = File(...),
    metadata: str = Form(...),
    user: User = Depends(get_current_user)
):
    """
    Full pipeline to ingest a PDF resume.
    1. Extracts text from PDF.
    2. Enriches data using LLM (extracts skills, experience, etc.).
    3. Merges manual metadata + extracted metadata + enriched metadata.
    4. Chunks text and generates embeddings.
    5. Upserts to Pinecone.
    """
    try:
        # 0. Parse manual metadata
        try:
            manual_metadata = json.loads(metadata)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON in metadata field")

        print(f"--- Starting Ingestion for {file.filename} ---")

        # 1. Extract Text & Metadata based on file type
        if file.content_type == "application/pdf" or file.filename.lower().endswith(".pdf"):
            extraction_result = extract_pdf_metadata(file)
        elif file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document" or file.filename.lower().endswith(".docx"):
            extraction_result = extract_docx_metadata(file)
        elif file.filename.lower().endswith(".doc"):
            # Optional: Add error or basic binary reading if strictly needed, but for now reject
            raise HTTPException(status_code=400, detail="Unsupported .doc (binary). Please save as .docx or .pdf")
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.content_type}. Use PDF or DOCX.")

        full_text = extraction_result["full_text"]
        
        if not full_text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from file (empty?)")

        # 2. LLM Enrichment
        print("--- Enriching with LLM ---")
        enriched_data = enrich_resume_data(full_text)
        
        # 3. Prepare Base Metadata (Merged)
        # We flatten the structure for Pinecone filtering where possible, 
        # or keep it as JSON string if Pinecone doesn't support nested objects efficiently for filtering 
        # (Pinecone supports string, number, boolean, lists of strings). 
        # Complex objects like 'experiencia_profissional' might need to be stored as a JSON string 
        # or simplified for filtering tags (e.g. valid_skills list).
        
        # Strategy: Keep high-level fields flat, and complex objects as JSON strings for retrieval contexts.
        # Key filterable fields: candidate_id, upload_date, skills (list), seniority_level, etc.
        
        base_metadata = {
            "source_file": file.filename,
            "upload_date": manual_metadata.get("upload_date", ""),
            "candidate_id": manual_metadata.get("id_candidato", ""), # Mapping manual Input
            # Enriched fields suitable for filtering
            "candidate_name": enriched_data.get("candidato", {}).get("nome_completo", ""),
            "email": (enriched_data.get("candidato", {}).get("email") or [""])[0], # Take first email
            "seniority_inferred": enriched_data.get("analise_ia", {}).get("senioridade_inferida", ""),
            "education_level": (enriched_data.get("formacao_academica") or [{}])[0].get("nivel", ""),
            
            # Store full enriched JSON for retrieval display
            "full_enriched_json": json.dumps(enriched_data, ensure_ascii=False)
        }
        
        # Add skills as a list of strings for filtering
        skills = enriched_data.get("perfil_profissional", {}).get("habilidades_tecnicas", [])
        if skills:
            base_metadata["skills"] = skills

        # 4. Chunking & Embedding
        print("--- Chunking and Embedding ---")
        chunks = split_text_into_chunks(full_text, chunk_size=500, overlap=50) # Smaller chunks for precision
        
        vectors_to_upsert = []
        
        for i, chunk in enumerate(chunks):
            vector_values = embeddingService(chunk)
            
            if not vector_values:
                print(f"Skipping chunk {i} due to embedding failure.")
                continue

            # Unique ID for the chunk
            chunk_id = str(uuid.uuid4())
            
            # Combine base metadata with chunk text
            chunk_metadata = base_metadata.copy()
            chunk_metadata["chunk_text"] = chunk
            chunk_metadata["chunk_index"] = i
            
            vectors_to_upsert.append({
                "id": chunk_id,
                "values": vector_values,
                "metadata": chunk_metadata
            })

        # 5. Upsert
        print(f"--- Upserting {len(vectors_to_upsert)} vectors ---")
        result = upsert_rich_vectors(vectors_to_upsert)
        
        if "error" in result:
             raise HTTPException(status_code=500, detail=result["error"])

        return {
            "status": "success",
            "vectors_upserted": len(vectors_to_upsert),
            "enriched_summary": enriched_data
        }

    except Exception as e:
        print(f"Error during ingestion: {e}")
        raise HTTPException(status_code=500, detail=str(e))
