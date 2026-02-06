
import asyncio
import os
from dotenv import load_dotenv
import sys
sys.path.append(os.getcwd())

from db.database import SessionLocal
from service.queryservice import hybrid_search

load_dotenv()

async def main():
    print("--- Check Hybrid Search ---")
    db = SessionLocal()
    try:
        # We assume there is some data, or at least we check if it runs without error
        print("1. Sending hybrid query...")
        results = await hybrid_search("candidato", db=db)
        
        print(f"SUCCESS: Found {len(results)} matches.")
        for r in results[:3]:
            print(f" - {r['id']} (Score: {r['score']}) - {r['metadata'].get('filename')}")

    except Exception as e:
        print(f"CRITICAL FAIL: Exception: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(main())
