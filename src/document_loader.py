import os
from .config import DOC_FOLDER, GREETING_FILE

class DocumentLoader:
    def __init__(self):
        self.doc_path = DOC_FOLDER

    def recursive_split(self, text, chunk_size=500, overlap=100):
        """
        Splits text using a priority-based 'switch' logic.
        Ensures no words are cut and structural integrity is maintained.
        """
        if len(text) <= chunk_size:
            return [text]

        chunks = []
        start = 0
        
        while start < len(text):
            # Define our search window
            end = start + chunk_size
            
            if end >= len(text):
                final_chunk = text[start:].strip()
                if final_chunk: chunks.append(final_chunk)
                break
            
            # --- THE SWITCH LOGIC ---
            # Find potential breakpoints within the current window
            p1 = text.rfind('\n\n', start, end) # Paragraph
            p2 = text.rfind('\n', start, end)   # Line break
            p3 = text.rfind('. ', start, end)   # Sentence end
            p4 = text.rfind(' ', start, end)    # Space (Word boundary)

            # We want to cut as close to the 'end' as possible, 
            # but prioritize structure over length.
            threshold = start + (chunk_size * 0.4)

            if p1 > threshold:
                chunk_end = p1
            elif p2 > threshold:
                chunk_end = p2
            elif p3 > threshold:
                chunk_end = p3 + 1 # Keep the period
            elif p4 > start:
                chunk_end = p4
            else:
                chunk_end = end # Emergency hard cut

            # Extract the chunk
            current_chunk = text[start:chunk_end].strip()
            if current_chunk:
                chunks.append(current_chunk)
            
         
            raw_start = chunk_end - overlap
            if raw_start <= start:
                start = chunk_end 
            else:
                # Find the first space AFTER the raw_start to align with a word
                safe_start = text.find(' ', raw_start)
                if safe_start == -1 or safe_start >= chunk_end:
                    start = chunk_end
                else:
                    start = safe_start + 1

        return [c for c in chunks if len(c) > 15]

    def load_documents(self):
        all_chunks = []
        metadata = []
        
        if not os.path.exists(self.doc_path):
            print(f"Directory not found: {self.doc_path}")
            return [], []

        for file in sorted(os.listdir(self.doc_path)):
            if file.endswith(".txt") and file != GREETING_FILE:
                path = os.path.join(self.doc_path, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        text = f.read()
                    
                    file_chunks = self.recursive_split(text)
                    all_chunks.extend(file_chunks)
                    metadata.extend([file] * len(file_chunks))
                except Exception as e:
                    print(f"Error reading {file}: {e}")
        
        return all_chunks, metadata