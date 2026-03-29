import os
from src.config import DOC_FOLDER, GREETING_FILE
from src.document_loader import DocumentLoader
from src.engine import EuonoiaEngine

def get_greeting():
    path = os.path.join(DOC_FOLDER, GREETING_FILE)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    return "Euonoia: System online."

def main():
    engine = EuonoiaEngine()
    loader = DocumentLoader()

    print("\n" + "="*50)
    print(get_greeting())
    print("="*50 + "\n")

    # Check cache first
    if not engine.load_existing_cache():
        chunks, meta = loader.load_documents()
        if not chunks:
            print("No data to process. Exiting.")
            return
        engine.build_index(chunks, meta)

    # CLI Chat
    while True:
        prompt = input("Ask Euonoia: ").strip()
        if prompt.lower() in ['exit', 'quit', 'bye']:
            break
            
        results = engine.search(prompt)

        print("\n--- Top Matches ---")
        for i, res in enumerate(results):
            print(f"[{i+1}] Source: {res['source']} (Score: {res['score']:.4f})")
            print(f"Content: {res['text']}\n")

if __name__ == "__main__":
    main()