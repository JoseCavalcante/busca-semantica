import requests
import json
import os

BASE_URL = "http://localhost:8000"
ENDPOINT = "/api/upsert/pdf_metadados"

def test_manual_metadata(pdf_path="curriculo_teste.pdf"):
    print("--- Testando Upsert com Metadados Manuais ---")
    
    # 1. Verificar se arquivo existe
    if not os.path.exists(pdf_path):
        print(f"❌ Arquivo '{pdf_path}' não encontrado.")
        print("Por favor, coloque um arquivo PDF nesta pasta ou edite o nome no script.")
        # Criando um arquivo dummy apenas para não crashar se for só teste de conexão (mas vai falhar no backend se não for pdf real)
        with open("curriculo1.pdf", "wb") as f:
            f.write(b"%PDF-1.4 empty pdf")
        pdf_path = "curriculo1'.pdf" 
        print("Arquivo 'curriculo1.pdf' criado temporariamente.")

    # 2. Definir os metadados manuais
    manual_metadata = {
        "id_candidato": "12345",
        "vaga_aplicada": "Desenvolvedor Python Senior",
        "origem": "LinkedIn",
        "data_upload": "2024-02-03"
    }

    # 3. Preparar a requisição
    # 'filePDF' é o arquivo
    # 'metadata' é uma STRING JSON
    
    files = {
        "filePDF": (pdf_path, open(pdf_path, "rb"), "application/pdf")
    }
    
    data = {
        "metadata": json.dumps(manual_metadata)
    }
    
    try:
        url = f"{BASE_URL}{ENDPOINT}"
        print(f"Enviando para {url}...")
        print(f"Arquivo: {pdf_path}")
        print(f"Metadados Manuais: {json.dumps(manual_metadata, indent=2)}")
        
        response = requests.post(url, files=files, data=data)
        
        if response.status_code == 200:
            print("\n✅ Sucesso!")
            print(f"Resposta: {response.json()}")
        else:
            print(f"\n❌ Erro: Status {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"\n❌ Falha na conexão: {e}")

if __name__ == "__main__":
    # Tenta achar algum PDF na pasta atual se o padrao nao existir
    target_pdf = "curriculo_teste.pdf"
    files = [f for f in os.listdir('.') if f.endswith('.pdf')]
    if files and not os.path.exists(target_pdf):
        target_pdf = files[0]
        
    test_manual_metadata(target_pdf)
