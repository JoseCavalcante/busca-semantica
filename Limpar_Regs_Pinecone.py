import os
from pinecone import Pinecone
from dotenv import load_dotenv

load_dotenv()

# Inicializa o client do Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# Conecta ao index usando o host específico do projeto
# Host obtido de services/upsertservice.py
index = pc.Index(host='https://busca-semantica-teste-5tjskwo.svc.aped-4627-b74a.pinecone.io')

# Namespace usado no projeto
NAMESPACE = "transcripts-Class-AI"

try:
    # Deleta todos os vetores do namespace específico
    index.delete(delete_all=True, namespace=NAMESPACE)
    print(f"Todos os registros do namespace '{NAMESPACE}' foram apagados com sucesso.")
except Exception as e:
    print(f"Ocorreu um erro ao tentar apagar os registros: {e}")
