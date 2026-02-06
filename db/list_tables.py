import sqlite3
import os

# Obtém o diretório onde este script está localizado
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "RHDB.db")

def list_tables():
    print(f"Conectando ao banco: {DB_NAME}")
    if not os.path.exists(DB_NAME):
        print("ERRO: Banco de dados não encontrado.")
        return

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # Consulta para listar tabelas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        conn.close()

        if tables:
            print(f"Total de tabelas encontradas: {len(tables)}")
            for table in tables:
                print(f"- {table[0]}")
        else:
            print("Nenhuma tabela encontrada.")
            
    except sqlite3.Error as e:
        print(f"Erro ao acessar o banco: {e}")

if __name__ == "__main__":
    list_tables()
