"""
Persistence for per-document FAISS indices and their chunk text.
 
FAISS only stores vectors, not the original chunk strings, so chunk text
is saved alongside the index (here as JSON for simplicity -- swap for a
Postgres table of (doc_id, chunk_index, chunk_text) rows to match the
project's storage architecture: raw files in blob storage, structured
data/references in Postgres).
"""

import faiss
import os
import json

INDEX_DIR = "indexes"                                       # folder for .faiss files
CHUNKS_DIR = "chunks"                                       # folder for .json files

def save_idx(index: faiss.Index, doc_id: str) -> str:
    os.makedirs(INDEX_DIR, exist_ok=True)                   # creates the indexes folder
    path = os.path.join(INDEX_DIR, f"{doc_id}.faiss")
    faiss.write_index(index, path)
    return path

# for the same doc_id, reconstructing the exact path and gives back a working faiss.Index object
def load_idx(doc_id: str) -> faiss.Index:
    path = os.path.join(INDEX_DIR, f"{doc_id}.faiss")
    return faiss.read_index(path)

# storing chunk texts into a json file
def save_chunks(chunks: list[str], doc_id: str) -> str:
    os.makedirs(CHUNKS_DIR, exist_ok=True)
    path = os.path.join(CHUNKS_DIR, f"{doc_id}.json")
    with open(path, "w") as f:
        json.dump(chunks, f)
    return path

# reading json array and giving back the associated chunk text
def load_chunks(doc_id: str) -> list[str]:
    path = os.path.join(CHUNKS_DIR, f"{doc_id}.json")
    with open(path) as f:
        return json.load(f)


 