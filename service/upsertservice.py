from service.authenticationservice import authentication_pinecone
from service.embeddingservice import embeddingService
import uuid

pc = authentication_pinecone()

def upsertService(embeddings:list):

    index = pc.Index(host='https://busca-semantica-teste-5tjskwo.svc.aped-4627-b74a.pinecone.ios')
    
    try:
        vectors = []
        for chunck_unit in embeddings:
            vectors.append({"id":f"{uuid.uuid4()}", "values": chunck_unit})

        response = index.upsert(vectors=vectors, namespace="transcripts-Class-AI")
        
        return {"message": "documento inserido com sucesso."}
    except Exception as e:
        return {"error":str(e)}
    


def upsertService_Metadados(metadata: dict, chuncklisttext: list):
    index = pc.Index(host='https://busca-semantica-teste-5tjskwo.svc.aped-4627-b74a.pinecone.io')
    vectors = []

    try:
        for chunckstext in chuncklisttext:
            if not chunckstext or not chunckstext.strip():
                # Pula chunks vazios ou em branco
                print("Chunk vazio detectado e ignorado.")
                continue

            embeddingchunck = embeddingService(chunckstext)
            metadatacomplete = {**metadata, "chunck": chunckstext.strip()}

            vectors.append({
                "id": str(uuid.uuid4()),
                "values": embeddingchunck,
                "metadata": metadatacomplete
            })

        if not vectors:
            return {"error": "Nenhum chunk válido para inserir."}

        response = index.upsert(vectors=vectors, namespace="transcripts-Class-AI")
        return response.upserted_count

    except Exception as e:
        return {"error": str(e)}




    """ 
def upsertService_Metadados(metadata:dict, chuncklisttext:list):

    index = pc.Index(host='https://curso2026-5tjskwo.svc.aped-4627-b74a.pinecone.io')

    vectors = []

    try:

        for chunckstext in chuncklisttext:
            embeddingchunck = embeddingService(chunckstext)
            metadatacomplete = {**metadata, "chunck": chunckstext}

            '''
            {"aula":"aula1", "professor":"nickson", "chunck":"texto aula 1}
            {"aula":"aula2", "professor":"nickson", "chunck":"texto aula 2}
            {"aula":"aula3", "professor":"nickson", "chunck":"texto aula 3}

            '''
            vectors.append({"id":f"{uuid.uuid4()}", 
                           "values": embeddingchunck, 
                           "metadata": metadatacomplete})
            
        response = index.upsert(vectors=vectors, namespace="transcripts-Class-AI")

        return response.upserted_count
    
    except Exception as e:  
        return {"error": str(e)} """

def upsert_rich_vectors(vectors: list):
    """
    Upserts a list of pre-constructed vectors (dict with id, values, metadata).
    """
    index = pc.Index(host='https://busca-semantica-teste-5tjskwo.svc.aped-4627-b74a.pinecone.io')
    
    # Use batches of 100 to avoid limits
    batch_size = 100
    total_upserted = 0
    
    try:
        for i in range(0, len(vectors), batch_size):
            batch = vectors[i:i + batch_size]
            response = index.upsert(vectors=batch, namespace="transcripts-Class-AI")
            total_upserted += response.upserted_count
            
        return {"message": f"Successfully inserted {total_upserted} vectors with rich metadata."}
    except Exception as e:
        return {"error": str(e)}