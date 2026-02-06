
import sys
import os
import json

sys.path.append(os.getcwd())

try:
    from service.queryservice import query_simples
    from service.assistenteservice import assistente_question

    search_term = "quem sabe python?"
    print(f"--- 1. Testing Search with term: '{search_term}' ---")
    
    # force lower threshold check by printing score
    # But we can't easily change the code from here. We just see the result.
    search_result = query_simples(search_term)
    
    print(f"Search Result Type: {type(search_result)}")
    if isinstance(search_result, dict):
        if 'matches' in search_result:
            print(f"Found {len(search_result['matches'])} matches.")
            for i, m in enumerate(search_result['matches']):
                print(f"  Match {i+1}: Score={m.get('score', 0):.4f} ID={m.get('id')}")
        else:
             print(f"No 'matches' key. Keys: {search_result.keys()}")
             print(f"Content: {search_result}")
    else:
        print(f"Result is not dict: {search_result}")

    print("\n--- 2. Testing Assistant Generation ---")
    response = assistente_question(search_term, search_result)
    
    print("Assistant Response Object:")
    print(response)
    
    if hasattr(response, 'content'):
        print(f"\nFinal Answer Text:\n{response.content}")
    
except Exception as e:
    import traceback
    traceback.print_exc()
