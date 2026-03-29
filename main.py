import os
from src.config import DOC_FOLDER, GREETING_FILE
from src.document_loader import DocumentLoader
from src.engine import EuonoiaEngine


# --------------------------------------------------
# TERMINAL UTILITIES
# --------------------------------------------------
def clear_terminal():
    """Clears the terminal screen based on the Operating System."""
    os.system('cls' if os.name == 'nt' else 'clear')


def get_greeting():
    path = os.path.join(DOC_FOLDER, GREETING_FILE)

    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()

    return "Euonoia: System online."


def print_welcome():
    print("\n" + "=" * 50)
    print(get_greeting())
    print("=" * 50 + "\n")


# --------------------------------------------------
# RESPONSE HANDLER
# --------------------------------------------------
def respond(engine, prompt):
    """
    Gets the best possible answer from the engine
    and prints it in a ChatGPT-style format.
    """

    best = engine.search_best(prompt)

    print("\n" + "-" * 50)

    if not best:
        print("Euonoia: I couldn't find a confident answer in the knowledge base.")
        print("-" * 50 + "\n")
        return

    # Clean formatting
    print("Euonoia:\n")
    print(best["text"].strip())
    print(f"\n(Source: {best['source']})")
    print("-" * 50 + "\n")


# --------------------------------------------------
# MAIN PROGRAM
# --------------------------------------------------
def main():
    engine = EuonoiaEngine()
    loader = DocumentLoader()

    # Initial UI
    clear_terminal()
    print_welcome()

    # Load cache first (fast startup)
    if not engine.load_existing_cache():
        chunks, meta = loader.load_documents()

        if not chunks:
            print("No documents found in the knowledge base.")
            return

        engine.build_index(chunks, meta)

    print("Euonoia is ready. Type your question below.\n")

    # --------------------------------------------------
    # CHAT LOOP
    # --------------------------------------------------
    while True:
        prompt = input("Ask Euonoia: ").strip()

        # Exit
        if prompt.lower() in ["exit", "quit", "bye"]:
            print("\nEuonoia: Goodbye.\n")
            break

        # Clear screen
        if prompt.lower() == "clear":
            clear_terminal()
            print_welcome()
            continue

        # Skip empty input
        if not prompt:
            continue

        # Ask engine
        respond(engine, prompt)


# --------------------------------------------------
# RUN
# --------------------------------------------------
if __name__ == "__main__":
    main()