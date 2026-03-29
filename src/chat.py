# src/chat_loop.py
from src.terminal import clear_terminal, print_welcome
from src.dataset import save_dataset, load_and_update_index
from src.conversation import converse  # <-- handles predefined + FAISS responses


def chat_loop(engine, loader, doc_folder):
    """
    Main chat loop for Euonoia.
    Responsibilities:
    - Human-computer conversation
    - Feeding new datasets into the engine
    - Clearing the terminal display
    - Exiting the program
    """
    print("I am ready my friend to answer your questions.\n")

    while True:
        # Prompt for user input
        prompt = input("Euonoia: ").strip()

        if not prompt:
            continue  # skip empty inputs

        # -------------------
        # EXIT PROGRAM
        # -------------------
        if prompt.lower() in ["exit", "quit", "bye"]:
            print("\nEuonoia: Goodbye.\n")
            break

        # -------------------
        # CLEAR TERMINAL
        # -------------------
        if prompt.lower() == "clear":
            clear_terminal()
            print_welcome()
            continue

        # -------------------
        # FEED NEW DATA
        # -------------------
        if prompt.lower() == "feed":
            print("Paste your text below. Finish with a blank line:")
            lines = []
            while True:
                line = input()
                if not line.strip():
                    break
                lines.append(line)
            new_text = "\n".join(lines)

            if not new_text.strip():
                print("No text provided. Cancelled.\n")
                continue

            # Save the new dataset and update the index
            filename = save_dataset(new_text, doc_folder)
            chunks_count = load_and_update_index(engine, loader)
            print(f"Euonoia: New dataset '{filename}' added. Total chunks indexed: {chunks_count}\n")
            continue

        # -------------------
        # HUMAN-COMPUTER CONVERSATION
        # -------------------
        response = converse(engine, prompt)  # uses predefined + FAISS (if question)
        print("\n" + "-" * 50)
        print(f"Euonoia:\n{response}")
        print("-" * 50 + "\n")