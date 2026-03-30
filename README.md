
# Euonoia - Local RAG Intelligence Engine

**Tagline:** A lightweight private knowledge base optimized for low-resource hardware.

---

## Overview

This project is a Local RAG Intelligence Engine designed to run on low-spec hardware
while still providing fast AI responses. It uses embeddings, FAISS, and a local LLM.

---

## Features

- Fully offline AI
- Lightweight and fast
- Works on older laptops
- Uses FAISS vector search
- Uses Sentence Transformers for embeddings
- Uses a local LLM (Ollama)

---

## Installation

### Create virtual environment

python3 -m venv venv
source venv/bin/activate

### Install dependencies

pip install --upgrade pip
pip install ollama
pip install sentence-transformers
pip install faiss-cpu

---

## How to Run

python main.py

---

## Author

Personal project focused on learning how RAG systems work.
