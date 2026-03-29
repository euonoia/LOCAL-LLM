# main.py
from src.engine import EuonoiaEngine
from src.document_loader import DocumentLoader
from src.terminal import clear_terminal, print_welcome
from src.chat import chat_loop
from src.dataset import load_and_update_index
from src.config import DOC_FOLDER

def main():
    engine = EuonoiaEngine()
    loader = DocumentLoader()

    clear_terminal()
    print_welcome()

    # Load cache or rebuild index
    if not engine.load_existing_cache():
        chunks_count = load_and_update_index(engine, loader)
        if not chunks_count:
            print("No documents found in my brain. Use 'feed' to teach me something!")

    chat_loop(engine, loader, DOC_FOLDER)

if __name__ == "__main__":
    main()