import faiss
import json
import os
import numpy as np

INDEX_PATH = "app/db/faiss_index/resume.index"
META_PATH = "app/db/faiss_index/resume_chunks.json"

def save_index(vectors, chunks):
    arr = np.array(vectors).astype("float32")
    dim = arr.shape[1]

    index = faiss.IndexFlatL2(dim)
    index.add(arr)
    faiss.write_index(index, INDEX_PATH)

    with open(META_PATH, "w") as f:
        json.dump(chunks, f)

def search_index(query_vector, k=4):
    if not os.path.exists(INDEX_PATH):
        return []

    index = faiss.read_index(INDEX_PATH)

    with open(META_PATH, "r") as f:
        chunks = json.load(f)

    q = np.array([query_vector]).astype("float32")
    _, indices = index.search(q, k)

    return [chunks[i] for i in indices[0] if i < len(chunks)]