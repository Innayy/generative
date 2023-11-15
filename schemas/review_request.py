from pydantic import BaseModel


class ReviewRequest(BaseModel):
    question: str
    answer: str
    student_answer: str
