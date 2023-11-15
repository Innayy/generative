from enum import Enum

from langchain.pydantic_v1 import BaseModel


class PeelFeedbackTitle(str, Enum):
    PEEL_FEEDBACK = "PEEL Feedback"


class PeelFeedbackItem(BaseModel):
    Point: str = "PEEL Feedback"
    Explanation: str = "Explation Feedback"
    Example: str = "Example Feedback"
    Link: str = "Link Feedback"


class FeedbackItem(BaseModel):
    title: PeelFeedbackTitle
    content: PeelFeedbackItem


class PeelFeedback(BaseModel):
    feedback: list[FeedbackItem]
