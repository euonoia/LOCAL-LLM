import os
from datetime import datetime
from .config import DOC_FOLDER

def create_dataset_from_text(raw_text, doc_title=None):
    """
    Saves raw pasted text into a new .txt file in DOC_FOLDER.
    Auto-generates a filename if doc_title is not provided.
    Returns the path of the saved file.
    """
    if not raw_text.strip():
        return None

    # Generate filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if doc_title:
        filename = f"{doc_title}_{timestamp}.txt"
    else:
        filename = f"document_{timestamp}.txt"

    path = os.path.join(DOC_FOLDER, filename)

    # Ensure directory exists
    os.makedirs(DOC_FOLDER, exist_ok=True)

    # Save file
    with open(path, "w", encoding="utf-8") as f:
        f.write(raw_text.strip())

    print(f"Dataset saved as: {filename}")
    return path