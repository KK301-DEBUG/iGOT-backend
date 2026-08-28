from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import fitz

# extracting text from pdf
def extract_from_pdf(path) -> str:
    doc = fitz.open(path)
    return "\n".join(page.get_text() for page in doc)

# chunking extracted text into chunks of 700 words (using words instead of actual tokens as we don't hv access to tokenizer).
def chunking(text, chunk_size = 700, overlap = 100):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunks.append(" ".join(words[start : end]))
        start += chunk_size - overlap
    return chunks

# selecting chunks
def select_chunks(chunks, chunk_embeddings, num_q):
    num_chunks = len(chunks)
    if num_chunks == 0:
        raise ValueError("No text found")

    # case 1: no. of chunks <= no. of questions
    if num_chunks <= num_q:
        centroid = np.mean(chunk_embeddings, axis=0, keepdims=True).astype("float32")        # determining the overall vector of the material
        faiss.normalize_L2(centroid)
        _, density_order = index.search(centroid, num_chunks)          # gives sorted tuple of chunks from highest similarity to lowest
        bonus_needed = num_q - num_chunks
        bonus_indices = density_order[0][:bonus_needed]
        plan = list(range(num_chunks)) + list(bonus_indices)
        return plan

    # case 2: no. of chunks > no. of questions
    centroid = np.mean(chunk_embeddings, axis=0, keepdims=True).astype("float32")     
    faiss.normalize_L2(centroid)
    density_score = chunk_embeddings @ centroid.T.flatten()

    # splitting chunk indices into num_q continguous buckets
    boundaries = np.linspace(0, num_chunks, num_q + 1, dtype=int)
    plan = []
    for b in range(num_q):
        start, end = boundaries[b], boundaries[b + 1]
        if start == end:
            end = min(start + 1, num_chunks)
        bucket_indices = range(start, end)
        best_index = max(bucket_indices, key=lambda i: density_score[i])     # taking best chunk (vector closest to centroid) in the bucket
        plan.append(best_index)
    return plan
    

# --RAG pipeline--
pdf = input("Enter material for quiz : ")
text = extract_from_pdf(pdf)
chunks = chunking(text)

# embedding chunks
model = SentenceTransformer("all-MiniLM-L6-v2")                 # 384 dimension vector model
chunk_embeddings = model.encode(chunks).astype("float32")
faiss.normalize_L2(chunk_embeddings)                            # cosine similarity via inner product

index = faiss.IndexFlatIP(chunk_embeddings.shape[1])
index.add(chunk_embeddings)

num_q = input("Enter no. of questions you want in the quiz : ")
