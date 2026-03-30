from src.terminal import clear_terminal, print_welcome
from src.dataset import save_dataset, load_and_update_index
from src.conversation import converse 

def chat_loop(engine, loader, doc_folder):
    print("I am ready, my friend, to answer your questions.\n")

    while True:
        # 'You:' makes it feel like a real conversation
        prompt = input("You: ").strip()

        if not prompt:
            continue

        # --- EXIT ---
        if prompt.lower() in ["exit", "quit", "bye"]:
            print("\nEuonoia: Goodbye! Have a beautiful day. \n")
            break

        # --- CLEAR ---
        if prompt.lower() == "clear":
            clear_terminal()
            print_welcome()
            continue

        # --- DATA INGESTION (FEED) ---
        if prompt.lower() == "feed":
            print("\n" + "="*30)
            print("PASTE MODE: Type 'DONE' on a new line to save.")
            print("="*30)
            lines = []
            while True:
                line = input()
                if line.strip().upper() == "DONE":
                    break
                lines.append(line)
            
            new_text = "\n".join(lines)
            if not new_text.strip():
                print("No text detected. Operation cancelled.\n")
                continue

            # Visual feedback during indexing
            print("Euonoia is indexing your data...", end="\r")
            filename = save_dataset(new_text, doc_folder)
            chunks_count = load_and_update_index(engine, loader)
            print(f"Done! ✅ '{filename}' added. Total chunks: {chunks_count}\n")
            continue

        print("Euonoia is thinking...", end="\r", flush=True)
        
        try:
            response = converse(engine, prompt)

            # If 'converse' returns a string (Predefined Greetings/Hugs), print it here.
            # If it used the LLM, it already printed the result and returned "".
            if response and response.strip():
                # Overwrite the 'thinking' line with a clean separator
                print(" " * 30, end="\r") 
                print("-" * 50)
                print(f"Euonoia: {response}")
                print("-" * 50 + "\n")
        
        except Exception as e:
            print(f"\n[Error]: Something went wrong in the circuits: {e}")