import requests
import json

BASE_URL = "http://localhost:8000"

def test_advanced_search():
    print("--- Testando Busca Avançada ---")
    
    # 1. Definir o filtro e a busca
    # Ajuste o 'search_text' e os 'filters' conforme o que você tem no seu banco Pinecone
    payload = {
        "search_text": "experiencia", # Mude para algo que exista nos seus PDFs
        "filters": {
            # "page_number": {"$eq": 1} # Exemplo de filtro
             # "filename": "exemplo.pdf"
        },
        "top_k": 3
    }
    
    try:
        print(f"Enviando requisição para {BASE_URL}/api/query/advanced...")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(f"{BASE_URL}/api/query/advanced", json=payload)
        
        if response.status_code == 200:
            results = response.json()
            print("\n✅ Sucesso! Resultados encontrados:")
            print(json.dumps(results, indent=2, ensure_ascii=False))
        else:
            print(f"\n❌ Erro: Status {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"\n❌ Falha na conexão: {e}")
        print("Certifique-se de que o servidor está rodando (uvicorn app:app --reload)")

if __name__ == "__main__":
    test_advanced_search()
