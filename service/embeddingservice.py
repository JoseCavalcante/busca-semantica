from service.authenticationservice import authentication_openai

clientOpeAI = authentication_openai()

""" 
def embeddingService(chunk : str):
    embeding = clientOpeAI.embeddings.create(
        model='text-embedding-ada-002',
        input=chunk

    )
    response = embeding.to_dict()
    vector = response['data'][0]['embedding']
    return vector 
"""

async def embeddingService(chunk: str):
    try:
        # Garante que o chunk não ultrapasse o limite de tokens (opcional)
        if len(chunk) > 8192:
            chunk = chunk[:8192]

        # Geração do embedding
        response = await clientOpeAI.embeddings.create(
            model='text-embedding-ada-002',
            input=chunk
        )

        # Acesso direto ao vetor
        vector = response.data[0].embedding
        return vector

    except Exception as e:
        print(f"[Erro no embeddingService] Falha ao gerar embedding: {e}")
        return None

