import json
from service.authenticationservice import authentication_openai

# Initialize OpenAI client
client = authentication_openai()

def enrich_resume_data(text: str) -> dict:
    """
    Uses OpenAI to extract structured metadata from resume text.
    """
    
    prompt = f"""
    You are an expert HR AI assistant. Your task is to analyze the following resume text and extract structured metadata.
    The text comes from a PDF extraction and may contain noise, headers, footers, or broken lines.
    Return ONLY a valid JSON object matching the following schema. Do not include markdown formatting or explanations.
    
    Schema:
    {{
      "candidato": {{
          "nome_completo": "string (Extract the full name of the candidate)",
          "email": ["string"],
          "telefones": ["string"],
          "linkedin_url": "string or null",
          "github_url": "string or null",
          "portfolio_url": "string or null",
          "cidade": "string or null",
          "estado": "string or null"
      }},
      "contexto": {{
          "resumo_profissional": "string (A concise summary of the candidate's profile)",
          "objetivo_profissional": "string",
          "area_atuacao": "string",
          "senioridade": "string (Junior/Pleno/Senior/Especialista - Infer based on experience)",
          "anos_experiencia": integer (total years of experience estimate),
          "disponibilidade": "string"
      }},
      "perfil_profissional": {{
          "habilidades_tecnicas": ["string (List specific technical skills, e.g., Python, AWS, React)"],
          "habilidades_comportamentais": ["string"],
          "idiomas": [
              {{"idioma": "string", "nivel": "string"}}
          ],
          "certificacoes": ["string"]
      }},
      "formacao_academica": [
          {{
              "instituicao": "string",
              "curso": "string",
              "nivel": "string",
              "status": "string",
              "ano_conclusao": integer or null
          }}
      ],
      "experiencia_profissional": [
          {{
              "empresa": "string",
              "cargo": "string",
              "data_inicio": "string (YYYY-MM)",
              "data_fim": "string (YYYY-MM or 'Atual')",
              "descricao": "string (Brief description of responsibilities)",
              "tecnologias_utilizadas": ["string"]
          }}
      ],
      "analise_ia": {{
          "score_geral": integer (0-100, assessment of profile completeness and quality),
          "pontos_fortes": ["string"],
          "pontos_atencao": ["string"],
          "senioridade_inferida": "string",
          "aderencia_cultura_tech": "string (Baixa/Média/Alta)"
      }}
    }}

    If a field is not found, use null or empty list.
    
    Resume Text:
    {text[:15000]}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", # Improved model for better structured output
            messages=[
                {"role": "system", "content": "You are a helpful HR assistant that extracts JSON data from resumes. You handle noisy text gracefully."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.1
        )
        
        content = response.choices[0].message.content
        return json.loads(content)
        
    except Exception as e:
        print(f"[Error in enrichment]: {e}")
        # Return empty structure or error indicator to avoid breaking pipeline
        return {"error": str(e), "candidato": {}, "contexto": {}}
