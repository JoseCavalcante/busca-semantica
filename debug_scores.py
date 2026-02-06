
import sys
import os
import json

sys.path.append(os.getcwd())

try:
    from service.authenticationservice import authentication_pinecone
    from service.embeddingservice import embeddingService
    
    pc = authentication_pinecone()
    index = pc.Index(host='https://busca-semantica-teste-5tjskwo.svc.aped-4627-b74a.pinecone.io')
    
    # Use a generic query typical of a job title
    search_term = "Desenvolvedor Python Senior"
    print(f"--- Querying for: '{search_term}' ---")
    
    vectors = embeddingService(search_term)
    
    # Get raw results without client-side filtering
    response = index.query(namespace="transcripts-Class-AI", vector=vectors, top_k=50, include_metadata=True)
    
    matches = response.get('matches', [])
    print(f"Total Matches from Pinecone: {len(matches)}")
    
    print("\nScore Distribution:")
    for i, m in enumerate(matches):
        print(f"#{i+1}: {m.score:.4f} - {m.metadata.get('filename') or m.metadata.get('candidate_name') or m.id}")

    # Check how many would pass the current 0.75 threshold
    passing = [m for m in matches if m.score > 0.75]
    print(f"\nMatches > 0.75: {len(passing)}")

except Exception as e:
    import traceback
    traceback.print_exc()
