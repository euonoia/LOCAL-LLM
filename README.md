# Euonoia: Local RAG Intelligence Engine 

**Tagline:** A lightweight, private knowledge base optimized for resource-constrained hardware (Dell Latitude E7450).

---

##  Overview

**Euonoia** is a local Retrieval-Augmented Generation (RAG) engine built to explore the fundamentals of Large Language Models (LLMs) and Machine Learning. 

The primary engineering challenge was to achieve **sub-20-second AI responses** on a 2015-era Dual-Core CPU with 16GB of RAM. This was made possible by implementing:
* **Model Quantization:** Utilizing the lightweight `gemma:2b` model via Ollama.
* **Greedy Decoding:** Setting temperature to `0.0` for deterministic, high-speed inference.
* **Efficient Vector Search:** Leveraging FAISS (Facebook AI Similarity Search) for near-instant document retrieval.

---

##  Tech Stack

* **OS:** Fedora Linux (Performance Optimized)
* **LLM Orchestration:** Ollama (`gemma:2b`)
* **Vector Database:** FAISS (CPU-optimized)
* **Embeddings:** Sentence-Transformers (`all-MiniLM-L6-v2`)
* **Environment:** Python 3.x (Virtual Environment)

---

## Project Structure

```text
euonoia/
├── main.py              # Application entry point
├── venv/                # Python Virtual Environment
├── documents/           # Knowledge base (.txt files) contains sensitive data i did not push it
├── data/storage/        # Persistent embeddings cache (.pkl)
├── src/
│   ├── config.py        # System paths and model configurations
│   ├── chat.py          # Terminal UI and chat loop logic
│   ├── conversation.py  # LLM streaming and Ollama integration
│   ├── dataset.py       # Document indexing and storage logic
│   ├── dataset_generator.py # Automated raw text to .txt conversion
│   ├── engine.py        # FAISS vector search implementation
│   └── terminal.py      # Terminal utility functions (clear/welcome)
└── README.md            # Project documentation
