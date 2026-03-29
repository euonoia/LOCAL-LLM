import os

# --- PATHS ---
# Your specific path for documents
DOC_FOLDER = "/mnt/HelloMaster/llm-project/documents"

# Keep the cache relative to where you run the script
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_DIR = os.path.join(BASE_DIR, "data/storage")
CACHE_PATH = os.path.join(CACHE_DIR, "embeddings_cache.pkl")

GREETING_FILE = "greeting.txt"

# --- MODEL CONFIG ---
MODEL_NAME = "all-MiniLM-L6-v2"

# Ensure the storage directory exists for the pickle file
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)