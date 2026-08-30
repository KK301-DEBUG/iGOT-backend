from google import genai
from mcq_schema import MCQ

client = genai.Client()                                     # reads GEMINI_API_KEY from env

MAX_ATTEMPTS_PER_SLOT = 3

def generate_mcq(chunk_text: str, competency_list: list[str]) -> dict:
    prompt = (
        f"Generate one MCQ from this training material for a "
        f"government statistical officer. Tag it with the closest matching competency "
        f"from this list : {competency_list}. \n\nMaterial : \n{chunk_text}"
    )
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "response_mime_type" : "application/json",
            "response_schema" : MCQ,
        },
    )
    mcq = MCQ.model_validate_json(response.text)
    return mcq.model_dump()

# check whether generated mcq is valid or not
def validate_mcq(mcq: dict, competency_list: list[str]) -> str | None:
    """returns None if valid, or a string reason if invalid."""
    if mcq["correct_answer"] not in mcq["options"]:
        return f"correct_answer '{mcq['correct_answer']}' not in options"
    if len(set(mcq["options"].values())) != 4:
        return "duplicate option text"
    if mcq["competency_tag"] not in competency_list:
        return f"competency_tag '{mcq['competency_tag']}' not in taxonomy"
    return None

# in case of invalid mcq take 3 attempts to replace it by a valid mcq

def generate_valid_mcq(candidates: list[int], 
                       chunks: list[str], 
                       competency_list: list[str], 
                       used_chunks: set[int] | None = None,
                       max_attempts: int = MAX_ATTEMPTS_PER_SLOT):

    # Tries candidate chunks in order for one question "slot" until a valid not-already-used MCQ is generated, or attempts are exhausted.
    if used_chunks is None:
        used_chunks = set()

    tried = 0
    attempts = []
    for chunk_idx in candidates:
        if chunk_idx in used_chunks:
            continue
        if tried >= max_attempts:
            break

        tried += 1

        try:
            mcq = generate_mcq(chunks[chunk_idx], competency_list)
        except Exception as e:
            attempts.append({"chunk_idx": chunk_idx, "reason": f"generation error: {e}", "mcq": None})
            continue

        reason = validate_mcq(mcq, competency_list)
        if reason is None:
            used_chunks.add(chunk_idx)
            return mcq, chunk_idx, attempts
        attempts.append({"chunk_idx": chunk_idx, "reason": reason, "mcq": mcq})

    return None, None, attempts


