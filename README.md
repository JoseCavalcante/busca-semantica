# Busca Semântica

Este projeto é uma plataforma de **Busca Semântica** desenvolvida em Python com FastAPI, projetada para facilitar o recrutamento e seleção através da análise inteligente de currículos e gestão de vagas.

A aplicação utiliza embeddings e bancos de dados vetoriais (Pinecone) para realizar buscas semânticas, permitindo encontrar candidatos que melhor se alinham às descrições das vagas, além da simples correspondência de palavras-chave.

## 🚀 Funcionalidades Principais

*   **Ingestão de Currículos**: Upload de arquivos (PDF e DOCX) com extração automática de texto.
*   **Busca Semântica**: Encontre candidatos ideais utilizando linguagem natural para descrever o perfil desejado.
*   **Gestão de Vagas**: Criação e administração de vagas de emprego.
*   **Assistente IA**: Interface de chat para auxiliar recrutadores.
*   **Autenticação**: Sistema de login e controle de acesso.
*   **Histórico**: Registro de atividades e buscas.

## 🛠️ Tecnologias Utilizadas

*   **Backend**: Python, FastAPI
*   **Banco de Dados Vetorial**: Pinecone (inferido)
*   **Banco de Dados Relacional**: SQLite (para dados estruturados)
*   **Front-end**: HTML, CSS, JavaScript (Vanilla)
*   **Outros**: LangChain, OpenAI API (provável para embeddings), Python-docx.

## 📋 Pré-requisitos

*   Python 3.8+
*   Conta no Pinecone e OpenAI (chaves de API)

## 🔧 Instalação e Configuração

1.  **Clone o repositório**
    ```bash
    git clone <url-do-repositorio>
    cd Busca_Semantica
    ```

2.  **Crie e ative o ambiente virtual**
    ```bash
    python -m venv venv
    # No Windows:
    .\venv\Scripts\activate
    # No Linux/Mac:
    source venv/bin/activate
    ```

3.  **Instale as dependências**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure as Variáveis de Ambiente**
    Crie um arquivo `.env` na raiz do projeto com as chaves necessárias (ex: `PINECONE_API_KEY`, `OPENAI_API_KEY`, `DATABASE_URL`, etc.). Consulte o administrador do projeto para obter as chaves corretas.

## ▶️ Como Executar

O projeto inclui um script facilitador para execução no Windows.

### Via Script (Windows)
Execute o arquivo `run_app.bat` na raiz do projeto:
```bash
.\run_app.bat
```
Isso iniciará o servidor FastAPI na porta 8001.

### Via Linha de Comando
Certifique-se de que o ambiente virtual está ativado e execute:
```bash
python -m uvicorn main:app --reload --port 8001
```

## 🌐 Acesso

*   **Aplicação Web (Login)**: [http://localhost:8001/](http://localhost:8001/) (Redireciona para `/static/login.html`)
*   **Documentação da API (Swagger UI)**: [http://localhost:8001/docs](http://localhost:8001/docs) or [http://localhost:8001/redoc](http://localhost:8001/redoc)

## 📂 Estrutura do Projeto

*   `main.py`: Ponto de entrada da aplicação FastAPI.
*   `api/`: Rotas (Endpoints) da API separadas por contexto (auth, ingest, job, query, etc.).
*   `service/`: Lógica de negócios e comunicação com serviços externos (Pinecone, OpenAI, DB).
*   `db/`: Configurações e modelos de banco de dados.
*   `static/`: Arquivos estáticos do frontend (HTML, CSS, JS).
*   `venv/`: Ambiente virtual Python.
