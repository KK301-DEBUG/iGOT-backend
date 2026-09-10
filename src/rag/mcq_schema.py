from pydantic import BaseModel
from typing import Literal

class MCQOptions(BaseModel):
    A: str
    B: str
    C: str
    D: str

class MCQ(BaseModel):
    question: str
    options: MCQOptions
    correct_answer: Literal["A", "B", "C", "D"]
    explanation: str
    difficulty: Literal["easy", "medium", "hard"]
    competency_tag: str

