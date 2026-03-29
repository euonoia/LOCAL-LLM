import os
from datetime import datetime

def save_dataset(text: str, doc_folder: str) -> str:
    """Save pasted text as a timestamped file"""
    os.makedirs(doc_folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"auto_dataset_{timestamp}.txt"
    path = os.path.join(doc_folder, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text.strip())
    return filename

def load_and_update_index(engine, loader):
    """Load documents and build FAISS index"""
    chunks, metadata = loader.load_documents()
    if not chunks:
        return 0
    engine.build_index(chunks, metadata)
    return len(chunks)