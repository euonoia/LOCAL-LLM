# Local LLM Semantic Search Project

This project explores the inner workings of Machine Learning and Large Language Models (LLMs) by building a local retrieval system. It transforms private text datasets into a searchable vector space for high-relevance data retrieval.

##  Project Origin
What began as a curiosity about how LLMs process information evolved into a functional local pipeline. By using a custom training dataset and tweaking the retrieval logic, this system allows for "semantic" understanding of local files rather than simple keyword matching.

##  System Architecture

The current architecture follows a linear pipeline from raw data to user query results:

1.  **Documents (.txt files):** Source data stored locally.
2.  **Text Splitting (Chunks):** Breaking down long documents into smaller segments to preserve local context.
3.  **Embeddings:** Utilizing **Sentence-Transformers** to convert text chunks into numerical vectors.
4.  **User Question:** The input query is converted into an embedding using the same model.
5.  **Similarity Search:** Performing a **Dot Product** calculation between the query vector and document vectors.
6.  **Retrieval:** Returning the most relevant chunk based on the highest similarity score.

---

## 🛠️ Requirements & Stack
* **Data Source:** Local `.txt` files (Custom Training Set).
* **Embedding Model:** Sentence-Transformers.
* **Logic:** Python scripts for processing and search.
* **Search Method:** Vector Similarity (Semantic Search).

## 🧬 Technical Logic
The system relies on the **Dot Product** to determine how "close" a user's question is to a specific piece of data:

$$A \cdot B = \sum_{i=1}^{n} A_i B_i$$

Where:
* $A$ is the Vector of the User Question.
* $B$ is the Vector of the Document Chunk.

##  Status
The system is currently functional. After initial testing and parameter tweaking, it successfully retrieves relevant information from the provided local dataset based on the semantic meaning of the user's query but the data is a mess its generating a same sentences every words that i ask.

![](./images/first_setup.png?raw=true)