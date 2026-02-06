import sqlite3
import os

# Obtém o diretório onde este script está localizado (c:\Projetos\Streamlit_RH\db)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define o caminho completo do banco de dados dentro da pasta db
DB_NAME = os.path.join(BASE_DIR, "RHDB.db")

def create_database():
    # Verifica se o arquivo já existe
    if os.path.exists(DB_NAME):
        print(f"O banco de dados já existe em: {DB_NAME}")
        return

    try:
        # Cria (ou conecta) o banco no caminho especificado
        conn = sqlite3.connect(DB_NAME)
        print(f"Banco de dados criado com sucesso em:\n{DB_NAME}")
        conn.close()
    except sqlite3.Error as e:
        print(f"Erro ao criar o banco: {e}")

if __name__ == "__main__":
    create_database()