"""
Selects which chunks to generate questions from, given a target number of
questions (num_q).
 
Hybrid approach:
- Positional bucketing (np.linspace) ensures full-document coverage when
  there are more chunks than questions.
- Centroid-based density scoring (dot product of chunk embeddings against
  the L2-normalized document centroid) weights toward information-dense
  regions, and is used to pick "bonus" chunks when there are fewer chunks
  than questions.
 
Returns a list of candidate lists, one per question "slot" -- each slot's
own chunk is tried first, with the remaining chunks (ranked by density) as
fallback if that chunk fails MCQ generation/validation.
"""

import numpy as np
import faiss

# selecting chunks
def select_chunks(chunks, chunk_embeddings, num_q):
    num_chunks = len(chunks)
    if num_chunks == 0:
        raise ValueError("No text found")
    
    centroid = np.mean(chunk_embeddings, axis=0, keepdims=True).astype("float32")     
    faiss.normalize_L2(centroid)
    density_score = chunk_embeddings @ centroid.T.flatten()

    # case 1: no. of chunks <= no. of questions
    if num_chunks <= num_q:
        density_order = list(np.argsort(-density_score))          # gives a list containing indices of density scores sorted highest to lowest 
        primary = list(range(num_chunks))
        bonus_needed = num_q - num_chunks
        bonus = density_order[:bonus_needed]                      # selects bonus questions based on density score
        slots = primary + bonus
        candidate_list = [[slot] + [i for i in density_order if i != slot] for slot in slots]   # builds one backup list per slot
        return candidate_list

    # case 2: no. of chunks > no. of questions

    # splitting chunk indices into num_q continguous buckets
    boundaries = np.linspace(0, num_chunks, num_q + 1, dtype=int)
    candidate_list = []
    for b in range(num_q):
        start, end = boundaries[b], boundaries[b + 1]
        if start == end:
            end = min(start + 1, num_chunks)
        bucket_indices = range(start, end)
        ranked = sorted(bucket_indices, key=lambda i: -density_score[i])   # ranking all chunks in the bucket by density score
        candidate_list.append(ranked)                                      # taking the best (vector closest to centroid) but keeping the rest for backup
    return candidate_list

