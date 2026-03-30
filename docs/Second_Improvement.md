# Engineering Improvements & Optimization Log

This document tracks the technical evolution of Euonoia from a high-latency prototype to a high-performance RAG engine optimized for the **Dell Latitude E7450**.

---

## 1. Inference Stability (The "Looping" Fix)
* **The Problem:** The model was generating repetitive sentences and getting stuck in "word loops," making the data unreadable.
* **The Solution:** Implemented **Greedy Decoding** by setting `temperature: 0.0` in the Ollama configuration.
* **The Result:** By forcing the model to select the most mathematically probable token instead of introducing randomness, we eliminated generation loops and significantly increased output logic.

## 2. Model Architecture Pivot
* **The Problem:** Running a 3.8B+ parameter model (Phi-3) on a 2015 Dual-Core CPU caused 60s+ latency and thermal throttling.
* **The Solution:** Switched to the **Gemma:2b** (2 Billion Parameter) architecture.
* **The Result:** * **RAM Savings:** Reduced footprint from ~2.3GB to **1.6GB**.
    * **Speed:** Dropped average response time from **60s down to ~16s**.

## 3. The "Logic Gate" Strategy (Hybrid Response)
* **The Problem:** Sending simple greetings (like "Hi") to the LLM wasted 15 seconds of CPU time for a 1-second task.
* **The Solution:** Built a **Predefined Knowledge Base** in `src/conversation.py`.
* **The Result:** Common social interactions and project FAQs now have **0ms latency**, bypassing the LLM entirely through an instant dictionary lookup.


## 4. Hybrid Re-Ranking Engine
* **The Problem:** Standard vector similarity (Dot Product) sometimes retrieved "noisy" chunks that were long but irrelevant.
* **The Solution:** Developed a custom `_rerank` algorithm in `src/engine.py`.
* **The Logic:**
    * **Keyword Overlap:** Direct matches for technical terms (e.g., "Hospital," "FAISS") receive a score boost.
    * **Length Penalty:** Prevents the AI from getting "lost" in massive text chunks by penalizing excessive character counts.
    * **Strict Threshold:** Added a **0.30 similarity cutoff** to prevent the LLM from hallucinating when no relevant data is found.

## 5. Hardware-Aware Threading
* **The Problem:** Default settings were not utilizing the specific architecture of the Intel i5-5300U.
* **The Solution:** Manually configured `num_thread: 4` in the `ollama.chat` options.
* **The Result:** Aligns perfectly with the **2-Core / 4-Thread** setup of the Dell E7450, ensuring maximum CPU utilization without crashing the Fedora kernel.

## 6. Vector Persistence (Pickle Caching)
* **The Problem:** The system had to re-encode every `.txt` file into vectors on every single launch (a heavy CPU "tax").
* **The Solution:** Integrated a persistent caching layer using `pickle` in `data/storage/`.
* **The Result:** Startup is now near-instant. The system only performs heavy encoding during the `feed` command for **new** data.

---

### 📊 Improvement Metrics
| Feature | v1.0 (Baseline) | v2.0 (Optimized) |
| :--- | :--- | :--- |
| **Model** | Phi-3 (3.8B) | **Gemma:2b** |
| **Response Time** | 60s+ | **16s** |
| **RAM Utilization** | High / Unstable | **1.6GB (Stable)** |
| **Search Logic** | Simple Similarity | **Hybrid Re-Ranking** |
| **Startup Time** | Slow (Re-indexing) | **Instant (Cached)** |

**Note:** These improvements were developed on **Fedora Linux** using a dedicated `venv` to ensure maximum system stability and performance.