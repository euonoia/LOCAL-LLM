import os
from src.config import DOC_FOLDER, GREETING_FILE

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_greeting():
    path = os.path.join(DOC_FOLDER, GREETING_FILE)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    return "Euonoia: System online."

def print_welcome():
    print("\n" + "="*50)
    print(get_greeting())
    print("="*50 + "\n")