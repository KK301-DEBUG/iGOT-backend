# chunking extracted text into chunks of 700 words (using words instead of actual tokens as we don't hv access to tokenizer).

def chunking(text: str, chunk_size: int = 700, overlap: int = 100) -> list[str]:
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunks.append(" ".join(words[start : end]))
        start += chunk_size - overlap
    return chunks