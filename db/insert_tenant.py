import sqlite3
import os
from datetime import datetime

# Obtém o diretório deste script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "RHDB.db")

def insert_tenant(name, tier="free"):
    print(f"Conectando ao banco: {DB_NAME}")
    
    # Limites definidos no models.py (copiados aqui para simplicidade do script)
    TIER_LIMITS = {
        "free": {"max_documents": 5, "max_prompts_per_day": 100},
        "pro": {"max_documents": 50, "max_prompts_per_day": 500},
        "enterprise": {"max_documents": 1000, "max_prompts_per_day": 10000}
    }
    
    limits = TIER_LIMITS.get(tier, TIER_LIMITS["free"])
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    try:
        sql = """
        INSERT INTO tenants (name, subscription_tier, max_documents, max_prompts_per_day, current_document_count, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        
        values = (
            name, 
            tier, 
            limits["max_documents"], 
            limits["max_prompts_per_day"], 
            0, # current_document_count
            datetime.utcnow()
        )
        
        cursor.execute(sql, values)
        conn.commit()
        print(f"✅ Tenant '{name}' ({tier}) inserido com sucesso! ID: {cursor.lastrowid}")
        
    except sqlite3.IntegrityError:
        print(f"❌ Erro: Tenant com nome '{name}' já existe.")
    except Exception as e:
        print(f"❌ Erro ao inserir tenant: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    print("--- Inserir Novo Tenant ---")
    nome = input("Nome da Empresa (Padrão: Demo Corp): ").strip()
    if not nome:
        nome = "Demo Corp"
        
    plano_input = input("Plano (free/pro/enterprise) [Padrão: free]: ").strip().lower()
    if plano_input not in ["free", "pro", "enterprise"]:
        plano_input = "free"
        
    insert_tenant(nome, plano_input)





    
