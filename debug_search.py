
import sys
import os

# Ensure we can import from root
sys.path.append(os.getcwd())

try:
    from service.queryservice import query_simples
    print("Testing query_simples...")
    result = query_simples("test search python")
    print(f"Result type: {type(result)}")
    print(f"Result keys: {result.keys() if isinstance(result, dict) else 'Not dict'}")
    if isinstance(result, dict) and 'error' in result:
        print(f"ERROR FOUND: {result['error']}")
    else:
        print("Success!")
except Exception as e:
    import traceback
    traceback.print_exc()
