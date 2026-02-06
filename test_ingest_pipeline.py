import requests
import json
import os

BASE_URL = "http://localhost:8000"
ENDPOINT = "/api/ingest"

def create_dummy_pdf(filename="dummy_cv.pdf"):
    try:
        from fpdf import FPDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Curriculo de Teste - Joao Silva", ln=1, align="C")
        pdf.cell(200, 10, txt="Skills: Python, FastAPI, Docker", ln=2, align="L")
        pdf.cell(200, 10, txt="Experience: Senior Developer at TechCorp (2020-Present)", ln=3, align="L")
        pdf.output(filename)
        print(f"Created temporary PDF: {filename}")
    except ImportError:
        # Fallback if fpdf not installed, write simple text file disguised as pdf (might fail extraction if strict)
        # But for valid testing let's assume we have a file or can just use one.
        with open(filename, "wb") as f:
            f.write(b"%PDF-1.4 ... dummy content ...") 
        print(f"Created dummy PDF (raw): {filename}")

def test_ingestion(pdf_path="Currículo1.pdf"):
    print(f"--- Testing Ingestion Pipeline: {pdf_path} ---")
    
    if not os.path.exists(pdf_path):
        print(f"File {pdf_path} not found. Creating a dummy one.")
        pdf_path = "dummy_cv.pdf"
        create_dummy_pdf(pdf_path)

    # Metadata that comes from the UI/Frontend
    manual_metadata = {
        "id_candidato": "candidate_007",
        "upload_date": "2024-02-04",
        "job_id": "REQ-123"
    }

    files = {
        "filePDF": (os.path.basename(pdf_path), open(pdf_path, "rb"), "application/pdf")
    }
    
    data = {
        "metadata": json.dumps(manual_metadata)
    }

    try:
        url = f"{BASE_URL}{ENDPOINT}"
        print(f"Sending POST to {url}...")
        
        response = requests.post(url, files=files, data=data)
        
        if response.status_code == 200:
            print("\n[SUCCESS] Pipeline Executed.")
            result = response.json()
            print(f"Vectors Upserted: {result.get('vectors_upserted')}")
            
            print("\n--- Enriched Information (Snippet) ---")
            enriched = result.get("enriched_summary", {})
            print(f"Candidate: {enriched.get('candidato', {}).get('nome_completo')}")
            print(f"Inferred Seniority: {enriched.get('analise_ia', {}).get('senioridade_inferida')}")
            print(f"Skills: {enriched.get('perfil_profissional', {}).get('habilidades_tecnicas')}")
            
        else:
            print(f"\n[ERROR] Status: {response.status_code}")
            print(response.text)

    except Exception as e:
        print(f"\n[CONNECTION ERROR]: {e}")
        print("Make sure the backend is running (uvicorn main:app --reload)")

if __name__ == "__main__":
    test_ingestion()
