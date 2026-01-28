import os
import ollama
import numpy as np
from dotenv import load_dotenv

# Load environment variables
load_dotenv(r'c:\big20\final\.env')

# Configuration
# Get the raw string from .env (e.g., 'f"http://{ETHOS_SERVER}:11435"')
raw_url = os.getenv('ETHOS_EMBEDDING_SERVER')
ethos_server = os.getenv('ETHOS_SERVER')

# Handle the f-string style string in .env if present
if raw_url:
    # Remove f" and " if they were literally included in the .env file
    clean_url = raw_url.strip('f').strip('"').strip("'")
    # Substitute {ETHOS_SERVER} with the actual IP
    final_url = clean_url.replace('{ETHOS_SERVER}', ethos_server)
else:
    # Fallback to a default if .env is missing or key is not found
    final_url = f"http://{ethos_server}:11435"

# Using explicit Client with resolved URL
client = ollama.Client(host=final_url)

MODEL_NAME = "nomic-embed-text:latest" 

def test_embedding_generation():
    print(f"--- Testing Embedding Generation with '{MODEL_NAME}' on {final_url} ---")
    
    sample_texts = [
        "안녕하세요, 저는 백엔드 개발자입니다.",
        "Spring Boot와 JPA를 사용한 경험이 있습니다.",
        "Hello, I am a backend developer.",
        "I have experience with Spring Boot and JPA."
    ]

    try:
        # Generate embeddings using the client
        embeddings = []
        for text in sample_texts:
            response = client.embeddings(model=MODEL_NAME, prompt=text)
            embedding = response['embedding']
            embeddings.append(embedding)
            print(f"Generate embedding for: '{text[:20]}...' -> Dimension: {len(embedding)}")

        # Basic Check: Dimensions should be consistent (e.g. 768 for nomic-embed-text)
        dim = len(embeddings[0])
        print(f"\nModel Dimension: {dim}")
        
        # Calculate Cosine Similarity
        # Similarity(A, B) = dot(A, B) / (norm(A) * norm(B))
        print("\n--- Similarity Check ---")
        
        def cosine_similarity(v1, v2):
            return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

        # Check: Korean vs English (Same Meaning)
        sim_ko_en = cosine_similarity(embeddings[0], embeddings[2])
        print(f"Similarity (KR vs EN 'Backend Dev'): {sim_ko_en:.4f} (Expected: High)")
        
        # Check: Related sentences (Backend vs Spring Boot)
        sim_related = cosine_similarity(embeddings[0], embeddings[1])
        print(f"Similarity (KR 'Backend' vs 'Spring'): {sim_related:.4f} (Expected: Medium-High)")

        if sim_ko_en > 0.6:
            print("\nSUCCESS: Model captures semantic similarity across languages.")
        else:
            print("\nWARNING: Multilingual similarity is lower than expected.")
            
    except Exception as e:
        print(f"\nERROR: Failed to generate embeddings.\nError: {e}")

if __name__ == "__main__":
    test_embedding_generation()
