import sqlite3
import os

# Obtém o diretório deste script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "RHDB.db")

def show_tenants():
    print(f"Conectando ao banco: {DB_NAME}")
    
    if not os.path.exists(DB_NAME):
        print("❌ Erro: Arquivo do banco de dados não encontrado.")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM users")
        tenants = cursor.fetchall()
        
        if not tenants:
            print("⚠️ Nenhum tenant encontrado.")
        else:
            print(f"\n{'ID':<5} {'Name':<30} {'Tier':<15} {'Docs':<10} {'Created At'}")
            print("-" * 80)
            for t in tenants:
                # t: (id, name, subscription_tier, current_document_count, max_documents, created_at)
                id, name, tier, curr_docs, max_docs, created_at = t
                docs_str = f"{curr_docs}/{max_docs}"
                print(f"{id:<5} {name:<30} {tier:<15} {docs_str:<10} {created_at}")
            print("-" * 80)
            print(f"Total: {len(tenants)} tenants.\n")
            
    except sqlite3.OperationalError as e:
        print(f"❌ Erro operacional (tabela existe?): {e}")
    except Exception as e:
        print(f"❌ Erro ao buscar tenants: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    show_tenants()
