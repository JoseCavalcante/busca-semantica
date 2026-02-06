from service.authenticationservice import authentication_pinecone
from service.embeddingservice import embeddingService

def deduplicate_matches(matches, target_top_k=5):
    """
    Deduplicates matches based on 'filename' in metadata.
    Keeps the highest scoring chunk for each file.
    """
    seen_files = set()
    unique_matches = []
    
    for match in matches:
        # Check for filename in various possible metadata keys to be robust
        # Prioritize 'filename', 'source', 'source_file', 'candidate_id', 'email'
        filename = (match.metadata.get('filename') or 
                    match.metadata.get('source') or 
                    match.metadata.get('source_file') or 
                    match.metadata.get('candidate_id') or 
                    match.metadata.get('email') or 
                    match.id)
        
        if filename not in seen_files:
            seen_files.add(filename)
            unique_matches.append(match)
            
        if len(unique_matches) >= target_top_k:
            break
            
    return unique_matches

def query_simples(search:str):

    pc = authentication_pinecone()

    try:

        vectors = embeddingService(search)

        index = pc.Index(host='https://busca-semantica-teste-5tjskwo.svc.aped-4627-b74a.pinecone.io')

        # Increase top_k to 50 to ensure we have enough candidates after deduplication
        response = index.query(namespace="transcripts-Class-AI", vector=vectors, top_k=50, include_metadata=True)

        # Adjusted threshold to 0.82 (High Precision) based on score analysis
        filtered_matches = [match for match in response['matches'] if match.score > 0.82]

        # Deduplicate results: Request 10 unique matches
        final_matches = deduplicate_matches(filtered_matches, target_top_k=10)

        if not final_matches:
            return {"message": "Nenhum resultado relevante encontrado."}

        # Convert to serializable format
        matches_data = []
        for m in final_matches:
            matches_data.append({
                "id": m.id,
                "score": m.score,
                "metadata": m.metadata or {}
            })

        return {"matches": matches_data}
    
    except Exception as e:
        return {"error":str(e)}    

def query_filtered(search:str, filters: dict, top_k: int = 5):
    pc = authentication_pinecone()
    
    try:
        vectors = embeddingService(search)
        index = pc.Index(host='https://busca-semantica-teste-5tjskwo.svc.aped-4627-b74a.pinecone.io')

        # Pass the filter dict directly to Pinecone
        # Request more matches (4x top_k) to allow for deduplication
        response = index.query(
            namespace="transcripts-Class-AI",
            vector=vectors,
            top_k=top_k * 4,
            include_metadata=True,
            filter=filters
        )
        
        # Adjusted threshold to 0.75 (High Precision)
        filtered_matches = [match for match in response['matches'] if match.score > 0.75]

        # Deduplicate results
        final_matches = deduplicate_matches(filtered_matches, target_top_k=top_k)

        if not final_matches:
            return {"message": "Nenhum resultado encontrado com esses filtros."}

        # Convert to serializable format
        matches_data = []
        for m in final_matches:
            matches_data.append({
                "id": m.id,
                "score": m.score,
                "metadata": m.metadata or {}
            })

        return {"matches": matches_data}

    except Exception as e:
        return {"error": str(e)}
