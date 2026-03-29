def respond(engine, prompt: str):
    """Searches for the best answer and prints it"""
    best = engine.search_best(prompt)
    print("\n" + "-" * 50)
    if not best:
        print("Euonoia: I am Sorry, feed me more data to answer your question.")
    else:
        # Print only the computer response
        lines = best["text"].splitlines()
        for line in lines:
            if line.lower().startswith("computer:"):
                print("Euonoia:\n" + line.replace("Computer:", "").strip())
                break
        else:
            print("Euonoia:\n" + best["text"].strip())
        print(f"\n(Source: {best['source']})")
    print("-" * 50 + "\n")