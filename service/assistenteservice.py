from service.authenticationservice import authentication_openai
from service.queryservice import query_simples

clienteOpenAI = authentication_openai()

def assistente_question(question:str, shortextract:str):
    
    # Cleaning the context
    context_text = ""
    if isinstance(shortextract, dict) and 'matches' in shortextract:
        for i, match in enumerate(shortextract['matches']):
            meta = match.get('metadata', {})
            text = meta.get('text', 'Sem conteúdo')
            filename = meta.get('filename') or meta.get('source') or f"Candidato {i+1}"
            score = match.get('score', 0)
            context_text += f"\n--- Candidato: {filename} (Match: {score:.2f}) ---\n{text}\n"
    elif isinstance(shortextract, list):
         for i, match in enumerate(shortextract):
            # Handle if match is obj or dict
            if hasattr(match, 'metadata'):
                meta = match.metadata
                score = match.score
            else:
                 meta = match.get('metadata', {})
                 score = match.get('score', 0)
            
            text = meta.get('text', 'Sem conteúdo')
            filename = meta.get('filename') or meta.get('source') or f"Candidato {i+1}"
            context_text += f"\n--- Candidato: {filename} (Match: {score:.2f}) ---\n{text}\n"
    else:
        context_text = str(shortextract)

    # Truncate if too long (simple safety)
    if len(context_text) > 30000:
        context_text = context_text[:30000] + "... (trecho cortado)"

    try:
        response = clienteOpenAI.chat.completions.create(
            model = "gpt-4o-mini",
            messages = [
                {"role":"system", "content": "Você é um assistente especialista em Recrutamento e Seleção (RH). "
                                             "Sua função é analisar os currículos fornecidos no contexto e responder às perguntas do usuário. "
                                             "Cite o nome dos candidatos quando relevante. "
                                             "Se a resposta não estiver no contexto, diga que não encontrou a informação."
                                             "Responda de forma direta e profissional."},
                {"role":"user", "content":f"Contexto (Currículos Encontrados):\n{context_text}\n\nPergunta: {question}"},
            ]
        )
        return response.choices[0].message
    except Exception as e:
        return {'error':str(e)}