
import os
import sys
# Ensure project root is in path
sys.path.append(os.getcwd())

from db.database import engine, SQLALCHEMY_DATABASE_URL
from sqlalchemy import text

def test_connection():
    print(f"--- Database Verification ---")
    print(f"configured URL: {SQLALCHEMY_DATABASE_URL}")
    
    is_sqlite = "sqlite" in SQLALCHEMY_DATABASE_URL
    is_postgres = "postgresql" in SQLALCHEMY_DATABASE_URL
    
    print(f"Detected Type: {'SQLite' if is_sqlite else 'Postgres' if is_postgres else 'Unknown'}")
    
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("Connection Successful! Result:", result.fetchone()[0])
            
            if is_sqlite:
                print("WARNING: You are still using SQLite. To use Postgres, set DATABASE_URL in .env")
            elif is_postgres:
                print("SUCCESS: You are connected to PostgreSQL.")
                
    except Exception as e:
        print(f"CRITICAL ERROR: Connection Failed. {e}")

if __name__ == "__main__":
    test_connection()
