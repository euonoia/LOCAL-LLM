import os
from .config import DOC_FOLDER, GREETING_FILE

def get_custom_greeting():
    path = os.path.join(DOC_FOLDER, GREETING_FILE)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    return "Euonoia: System online. How can I help you today?"