from service.authenticationservice import authentication_pinecone
from pinecone import ServerlessSpec

pc = authentication_pinecone()

def create_index(nameBD: str):
    if nameBD not in pc.list_indexes():
        try:
            pc.create_index(
                name=nameBD,
                dimension=1536,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1")
            )
            return f"Índice '{nameBD}' criado com sucesso."
            
        except Exception as e:
            print(f"Erro ao criar o índice: {e}")
    else:
        print(f"O índice '{nameBD}' já existe.")

def list_index():
    response = pc.list_indexes()
    return response.to_dict()

def detail_index(nameIDX:str):
    response = pc.describe_index(name = nameIDX)
    return response.to_dict()