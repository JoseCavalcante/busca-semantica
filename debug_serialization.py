
import sys
import os
import json

sys.path.append(os.getcwd())

try:
    from service.authenticationservice import authentication_pinecone
    from service.embeddingservice import embeddingService
    
    pc = authentication_pinecone()
    index = pc.Index(host='https://busca-semantica-teste-5tjskwo.svc.aped-4627-b74a.pinecone.io')
    
    # Use a common term likely to return matches
    vectors = embeddingService("desenvolvedor")
    res = index.query(namespace="transcripts-Class-AI", vector=vectors, top_k=2, include_metadata=True)
    
    print(f"Type of response: {type(res)}")
    print(f"Dir response: {dir(res)}")
    
    # Try assignment
    try:
        res['matches'] = []
        print("Assignment via dict key successful")
    except Exception as e:
        print(f"Assignment failed: {e}")

    # Try serialization
    try:
        json.dumps(res)
        print("JSON serialization successful")
    except Exception as e:
        print(f"JSON serialization failed: {e}")

    if hasattr(res, 'to_dict'):
         print("Has to_dict()")
         
except Exception as e:
    import traceback
    traceback.print_exc()
