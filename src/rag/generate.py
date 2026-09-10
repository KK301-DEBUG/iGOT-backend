import json
from chunk_selection import select_chunks
from mcq_generation import generate_valid_mcq, MAX_ATTEMPTS_PER_SLOT
from storage import load_idx, load_chunks

# dummy list to store competency tags from module 1
COMPETENCY_LIST = ["Survey Design", "Sampling Methodology", "Data Validation",
                    "National Accounts", "GIS/Geospatial Statistics", "Data Protection Law"]    

def generate_quiz(doc_id: str, num_q: int, competency_list: list[str] = COMPETENCY_LIST) -> dict:
    index = load_idx(doc_id)
    chunks = load_chunks(doc_id)
    chunk_embeddings = index.reconstruct_n(0, index.ntotal)
 
    candidate_list = select_chunks(chunks, chunk_embeddings, num_q)
 
    quiz = []
    failed_slots = []
    used_chunks = set()
 
    for slot_num, candidates in enumerate(candidate_list):
        mcq, used_chunk_idx, attempts = generate_valid_mcq(
            candidates, chunks, competency_list, used_chunks=used_chunks
        )
        if mcq is not None:
            quiz.append(mcq)
            if attempts:
                print(
                    f"Slot {slot_num}: succeeded on attempt {len(attempts) + 1} "
                    f"(chunk {used_chunk_idx}) after {len(attempts)} rejection(s)"
                )
        else:
            failed_slots.append({"slot": slot_num, "attempts": attempts})
 
    return {
        "doc_id": doc_id,
        "requested": num_q,
        "generated": len(quiz),
        "quiz": quiz,
        "failed_slots": failed_slots,
    }
 
if __name__ == "__main__":
    doc_id = input("Enter doc_id to generate a quiz from: ")
    num_q = int(input("Enter no. of questions you want in the quiz: "))
 
    result = generate_quiz(doc_id, num_q)
 
    print(f"\n{result['generated']} / {result['requested']} questions generated successfully")
    if result["failed_slots"]:
        print(f"{len(result['failed_slots'])} slot(s) failed after exhausting {MAX_ATTEMPTS_PER_SLOT} attempts:")
        for f in result["failed_slots"]:
            print(f"  - slot {f['slot']}: {[a['reason'] for a in f['attempts']]}")
 
    print(json.dumps(result["quiz"], indent=2))


