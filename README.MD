TITLE: Euonoia - Local RAG intelligence Engine

Tagline: A lightweight, private knowledge base optimized for resource-constrained hardware (Dell E7450).

"Euonoia is a Local Rag Intelligence Engine that I design to study the Fundamentals of the LLM and Machine Learnings Euonoia was designed to provide sub-20-second AI responses on a 2015 Dual-Core CPU with 16GB RAM using Model Quantization and Greedy Decoding."

Installation Setup:

    I developed this On Fedora Linux using a venv(Virtual Environment) to keep my system python clean and ensure my AI libraries like faiss and sentence transformer dont conflicts with my system updates

    1. System Preparation (Fedora)
    
    First, ensure your Fedora system has the necessary development tools for building Python extensions (required for faiss).

    sudo dnf update -y
    sudo dnf install -y python3-devel gcc gcc-c++           

    2. Virtual Environment Setup

    Navigate to your project folder (e.g., ~/Documents/euonoia) and run these commands:

    # 1. Create the virtual environment
    python3 -m venv venv

    # 2. Activate it (You'll see '(venv)' appear in your terminal)
    source venv/bin/activate

    3. Install Dependencies
    While the venv is active, install the specific libraries we used for your RAG system

    # Update pip first
    pip install --upgrade pip

    # Install the "Core Three" for your RAG engine
    pip install ollama
    pip install sentence-transformers
    pip install faiss-cpu  # I am using the cpu version because on my dell e7450

    4. Setup the Ollama "Brain"
    Ollama runs as a background service on Fedora. Ensure the Gemma:2b model is downloaded and ready.

    # In a new terminal window:
    ollama pull gemma:2b

    # Verify it is loaded
    ollama list

    6. Running the Program

    Now that everything is installed, you can start the engine. Remember to always activate the venv if you open a new terminal.

    # If not already active:
    source venv/bin/activate

    # Run the project
    python main.py
    