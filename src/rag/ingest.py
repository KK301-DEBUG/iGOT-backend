import faiss
from sentence_transformers import SentenceTransformer
from extraction import extract_text
from chunking import chunking
from storage import save_idx, save_chunks

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")                 # 384 dimension vector model
    return _model

def ingest_document(path: str, doc_id: str) -> dict:
    text = extract_text(path)
    chunks = chunking(text)
    model = get_model()
    chunk_embeddings = model.encode(chunks).astype("float32")
    faiss.normalize_L2(chunk_embeddings)                            # cosine similarity via inner product

    index = faiss.IndexFlatIP(chunk_embeddings.shape[1])
    index.add(chunk_embeddings)

    save_idx(index, doc_id)
    save_chunks(chunks, doc_id)

    return {"doc_id": doc_id, "num_chunks": len(chunks)}

if __name__ == "__main__":
    pdf_path = input("Enter material to ingest : ")
    doc_id = input("Enter doc_id for this material : ")
    result = ingest_document(pdf_path, doc_id)
    print(result)

