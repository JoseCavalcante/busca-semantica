
import asyncio
import os
from dotenv import load_dotenv
# Add project root to sys.path to ensure imports work
import sys
sys.path.append(os.getcwd())

from service.queryservice import query_simples

load_dotenv()

async def main():
    print("--- Check Async Architecture ---")
    try:
        # We perform a simple query to verify the whole stack:
        # AsyncOpenAI -> Async Embedding -> Async Query -> Pinecone (Sync wrapped in async function)
        print("1. Sending async query...")
        result = await query_simples("test verification")
        
        if "error" in result:
             print(f"FAIL: Error returned: {result['error']}")
        else:
             print("SUCCESS: Result received.")
             if "matches" in result:
                 print(f"Matches found: {len(result['matches'])}")
             else:
                 print(f"Response keys: {result.keys()}")

    except Exception as e:
        print(f"CRITICAL FAIL: Exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
