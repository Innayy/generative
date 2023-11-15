from enum import Enum

from langchain.pydantic_v1 import BaseModel


class GeneralFeedbackTitle(str, Enum):
    GENERAL_FEEDBACK = "General Feedback"
    SUGGESTED_ANSWER = "Suggested Answer"


class GeneralFeedbackItem(BaseModel):
    title: GeneralFeedbackTitle
    content: str


class GeneralFeedback(BaseModel):
    feedback: list[GeneralFeedbackItem]
