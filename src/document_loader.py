import os
from .config import DOC_FOLDER, GREETING_FILE

class DocumentLoader:
    def __init__(self):
        self.doc_path = DOC_FOLDER

    def split_text(self, text, chunk_size=300, overlap=50):
        words = text.split()
        return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size - overlap)]

    def load_documents(self):
        all_chunks = []
        metadata = []
        
        if not os.path.exists(self.doc_path):
            print(f"CRITICAL ERROR: Folder not found at {self.doc_path}")
            return [], []

        for file in os.listdir(self.doc_path):
            if file.endswith(".txt") and file != GREETING_FILE:
                path = os.path.join(self.doc_path, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        text = f.read()
                    
                    chunks = self.split_text(text)
                    all_chunks.extend(chunks)
                    metadata.extend([file] * len(chunks))
                except Exception as e:
                    print(f"Skipping {file} due to error: {e}")
        
        return all_chunks, metadata