import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "RHDB.db")

def inspect_contents():
    print(f"Conectando ao banco: {DB_NAME}")
    if not os.path.exists(DB_NAME):
        print(f"ERRO: Banco de dados não encontrado em {DB_NAME}")
        return

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # Listar tabelas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        if not tables:
            print("Nenhuma tabela encontrada no banco.")
            conn.close()
            return

        for table_tuple in tables:
            t_name = table_tuple[0]
            print(f"\n{'='*40}")
            print(f" TABELA: {t_name}")
            print(f"{'='*40}")
            
            # Obter nomes das colunas
            cursor.execute(f"PRAGMA table_info({t_name})")
            columns_info = cursor.fetchall()
            columns = [info[1] for info in columns_info] 
            print(f"Colunas: {columns}")
            print(f"{'-'*40}")
            
            # Obter dados
            cursor.execute(f"SELECT * FROM {t_name}")
            rows = cursor.fetchall()
            
            if rows:
                for row in rows:
                    print(row)
            else:
                print("(Tabela vazia)")
                
        conn.close()
        
    except sqlite3.Error as e:
        print(f"Erro SQLite: {e}")

if __name__ == "__main__":
    inspect_contents()
