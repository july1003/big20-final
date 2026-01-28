import os
import ollama
import numpy as np
import time
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv(r'c:\big20\final\.env')

# Setup reporting
timestamp = datetime.now().strftime("%y%m%d_%H%M")
report_dir = r'c:\big20\final\report'
os.makedirs(report_dir, exist_ok=True)
report_file = os.path.join(report_dir, f"embedding_test_result_{timestamp}.md")

def log(msg, end='\n'):
    print(msg, end=end)
    with open(report_file, 'a', encoding='utf-8') as f:
        f.write(msg + end)

# Configuration
raw_url = os.getenv('ETHOS_EMBEDDING_SERVER')
ethos_server = os.getenv('ETHOS_SERVER')

if raw_url:
    clean_url = raw_url.strip('f').strip('"').strip("'")
    final_url = clean_url.replace('{ETHOS_SERVER}', ethos_server)
else:
    final_url = f"http://{ethos_server}:11435"

# Using explicit Client with resolved URL
client = ollama.Client(host=final_url)

def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def run_test_for_model(model_name):
    log("\n" + "="*60)
    log(f" TESTING MODEL: {model_name}")
    log("="*60)
    
    sample_texts = [
        "안녕하세요, 저는 백엔드 개발자입니다.",
        "Spring Boot와 JPA를 사용한 경험이 있습니다.",
        "Hello, I am a backend developer.",
        "I have experience with Spring Boot and JPA."
    ]

    try:
        embeddings = []
        start_time = time.time()
        
        for text in sample_texts:
            item_start = time.time()
            response = client.embeddings(model=model_name, prompt=text)
            item_end = time.time()
            
            embedding = response['embedding']
            embeddings.append(embedding)
            log(f" - Generated for: '{text[:15]}...' | Dim: {len(embedding)} | Time: {item_end - item_start:.4f}s")

        total_time = time.time() - start_time
        avg_time = total_time / len(sample_texts)
        
        log(f"\n[Performance] Total: {total_time:.4f}s | Avg: {avg_time:.4f}s per request")
        
        # Similarity Analysis
        sim_ko_en = cosine_similarity(embeddings[0], embeddings[2])
        sim_related = cosine_similarity(embeddings[0], embeddings[1])
        
        log(f"[Similarity] KR-EN Cross: {sim_ko_en:.4f}")
        log(f"[Similarity] Related (KR): {sim_related:.4f}")
        
        return {
            "model": model_name,
            "avg_time": avg_time,
            "sim_ko_en": sim_ko_en,
            "sim_related": sim_related,
            "dim": len(embeddings[0])
        }
            
    except Exception as e:
        log(f" ERROR testing {model_name}: {e}")
        return None

def main():
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(f"# Embedding Model Performance Report\n")
        f.write(f"- Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"- Ethos Server: {final_url}\n\n")

    log(f"Fetching tags from {final_url}...")
    try:
        tags = client.list()
        
        available_models = []
        models_list = tags.models if hasattr(tags, 'models') else tags.get('models', [])
        
        for m in models_list:
            name = None
            if hasattr(m, 'model'): name = m.model
            elif hasattr(m, 'name'): name = m.name
            elif isinstance(m, dict):
                name = m.get('model') or m.get('name')
            
            if name:
                available_models.append(name)
        
        if not available_models:
            log(f"No models found on the server. Raw response: {tags}")
            return

        log(f"Found {len(available_models)} models: {', '.join(available_models)}")
        
        results = []
        for model in available_models:
            if any(kw in model.lower() for kw in ['embed', 'bert', 'bge']):
                res = run_test_for_model(model)
                if res:
                    results.append(res)
            else:
                log(f"\n Skipping non-embedding model: {model}")

        if not results:
            log("\nNo embedding models detected to test.")
            return

        results.sort(key=lambda x: x['avg_time'])
        log("\n\n" + "#"*60)
        log(" FINAL COMPARISON SUMMARY (Sorted by Speed)")
        log("#"*60)
        log(f"{'Model Name':<30} | {'Dim':<5} | {'Avg Time':<10} | {'KR-EN Sim':<10}")
        log("-" * 65)
        for r in results:
            log(f"{r['model']:<30} | {r['dim']:<5} | {r['avg_time']:>8.4f}s | {r['sim_ko_en']:>10.4f}")
        log("#"*60)
        
        log(f"\nReport saved to: {report_file}")

    except Exception as e:
        import traceback
        log(f"Failed to fetch model list: {e}")
        # Write traceback to file manually since log doesn't handle objects
        with open(report_file, 'a', encoding='utf-8') as f:
            traceback.print_exc(file=f)
        traceback.print_exc()

if __name__ == "__main__":
    main()
