
import sqlite3
import os

DB_PATH = "db/RHDB.db"

def add_columns():
    if not os.path.exists(DB_PATH):
        print(f"Database {DB_PATH} not found. Running init_db instead.")
        # Fallback to creating new if not exists
        from init_db import init_db
        init_db()
        return

    print(f"Updating schema for {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Add processing_status
        cursor.execute("ALTER TABLE candidate_documents ADD COLUMN processing_status TEXT DEFAULT 'PENDING'")
        print("Added column: processing_status")
    except sqlite3.OperationalError as e:
        print(f"Column processing_status might already exist: {e}")

    try:
        # Add processing_error
        cursor.execute("ALTER TABLE candidate_documents ADD COLUMN processing_error TEXT")
        print("Added column: processing_error")
    except sqlite3.OperationalError as e:
        print(f"Column processing_error might already exist: {e}")

    conn.commit()
    conn.close()
    print("Schema update complete.")

if __name__ == "__main__":
    add_columns()
