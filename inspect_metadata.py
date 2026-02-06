import sys
import os
import json
from service.authenticationservice import authentication_pinecone

# Ensure we can import from service
sys.path.append(os.getcwd())

def inspect_metadata():
    print("--- Inspecting Pinecone Metadata ---")
    
    try:
        pc = authentication_pinecone()
        # Hardcoded host from upsertservice.py
        host = 'https://busca-semantica-teste-5tjskwo.svc.aped-4627-b74a.pinecone.io'
        index = pc.Index(host=host)
        
        namespace = "transcripts-Class-AI"
        
        print(f"Connected to index. Querying namespace: {namespace}...")
        
        # Create a dummy vector of size 1536 (typical for OpenAI)
        # We don't care about matches, just want any record with metadata
        dummy_vector = [0.1] * 1536
        
        response = index.query(
            vector=dummy_vector,
            top_k=1,
            include_metadata=False, # We want to focus on values
            include_values=True,
            namespace=namespace
        )
        
        if response.matches:
            match = response.matches[0]
            print(f"\n✅ Found record ID: {match.id}")
            
            if match.values:
                print(f"Vector Dimensions: {len(match.values)}")
                print("Vector Values (First 20):")
                print(match.values[:20])
                print("...")
            else:
                print("Values not returned (check include_values=True)")
        else:
            print("\n⚠️ No records found in this namespace.")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    inspect_metadata()
