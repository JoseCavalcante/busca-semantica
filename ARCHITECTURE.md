# Arquitetura do Sistema - Busca Semântica

Este documento descreve a arquitetura técnica do projeto **Busca Semântica**, detalhando seus componentes, fluxos de dados e decisões de design.

## 1. Visão Geral

O sistema é uma aplicação monolítica modular baseada em **FastAPI**, utilizando uma arquitetura em camadas (Controller-Service-Repository) para separar responsabilidades. O foco principal é a ingestão, processamento e recuperação semântica de currículos.

## 2. Diagrama de Arquitetura

```mermaid
graph TD
    UserClient[Frontend / Cliente] -->|HTTP/REST| API[FastAPI (main.py)]
    
    subgraph "Camada de API (Routers)"
        API --> AuthRouter[Authentication Router]
        API --> IngestRouter[Ingest Router]
        API --> QueryRouter[Query Router]
        API --> JobRouter[Job Router]
    end
    
    subgraph "Camada de Serviço (Services)"
        IngestRouter --> ExtracaoService[Extração PDF/DOCX]
        IngestRouter --> EnrichService[Enriquecimento (LLM)]
        IngestRouter --> EmbedService[Embedding Service]
        IngestRouter --> UpsertService[Upsert Service]
        
        QueryRouter --> QueryService[Query Service]
        QueryService --> EmbedService
    end
    
    subgraph "Camada de Dados"
        AuthRouter --> SQLite[(SQLite DB)]
        JobRouter --> SQLite
        UpsertService --> Pinecone[(Pinecone Vector DB)]
        QueryService --> Pinecone
    end
    
    subgraph "Serviços Externos"
        EnrichService --> OpenAI[OpenAI API]
        EmbedService --> OpenAI
    end
```

## 3. Componentes Principais

### 3.1 Backend (FastAPI)
O backend é o núcleo do sistema, responsável por orquestrar todas as operações.
- **`main.py`**: Ponto de entrada, configuração de middlewares (CORS) e montagem de rotas.
- **Routers (`api/`)**: Controladores REST que recebem requisições HTTP e validam dados.
- **Services (`service/`)**: Contêm a lógica de negócio pura.
    - `extracaoPDFservice.py`: Extrai texto bruto de documentos.
    - `enrichmentservice.py`: Usa LLMs para estruturar dados não estruturados (JSON).
    - `embeddingservice.py`: Gera vetores a partir de texto.
    - `upsertservice.py`: Gerencia a inserção e indexação no Pinecone.

### 3.2 Banco de Dados Relacional (SQLite)
Gerenciado via SQLAlchemy (`db/models.py`), armazena dados estruturados e relacionais:
- **Tenant**: Gerencia multilocatariedade e limites de uso.
- **User**: Usuários do sistema com controle de acesso (RBAC).
- **Job**: Vagas de emprego criadas pelos recrutadores.
- **ChatMessage/Prompt**: Histórico de interações.

### 3.3 Banco de Dados Vetorial (Pinecone)
Armazena os "chunks" de texto dos currículos processados e seus embeddings.
- **Namespace**: `transcripts-Class-AI`
- **Metadata**: Armazena dados ricos (skills, experiência, IDs) junto com o vetor para permitir filtragem híbrida.

### 3.4 Frontend
Atualmente servido como arquivos estáticos (`static/`) via FastAPI. Utiliza HTML/CSS/JS (Vanilla) para interagir com a API.

## 4. Fluxos de Dados Críticos

### 4.1 Ingestão de Currículos
1.  **Upload**: O usuário envia um PDF/DOCX via endpoint `/api/ingest`.
2.  **Extração**: O sistema lê o binário e converte para texto.
3.  **Enriquecimento**: O texto é enviado à OpenAI para extrair entidades (Nome, Email, Skills).
4.  **Chunking**: O texto é dividido em pedaços menores (chunks).
5.  **Embedding**: Cada chunk é convertido em vetor.
6.  **Armazenamento**: Vetores e metadados enriquecidos são salvos no Pinecone.

### 4.2 Busca Semântica
1.  **Query**: Usuário digita uma descrição de vaga.
2.  **Embedding da Query**: A descrição é vetorizada.
3.  **Busca Vetorial**: Pinecone recupera os vetores mais similares.
4.  **Reranking/Filtro**: (Opcional) Resultados são filtrados por metadados (ex: Senioridade).
5.  **Resposta**: Lista de candidatos ordenados por relevância é retornada.

## 5. Segurança
- **Autenticação**: Baseada em OAuth2 com JWT (JSON Web Tokens).
- **Controle de Acesso**: Decoradores `get_current_user` garantem que apenas usuários autenticados acessem rotas críticas.
- **Multitenancy**: Dados relacionais são segregados por `tenant_id`.
