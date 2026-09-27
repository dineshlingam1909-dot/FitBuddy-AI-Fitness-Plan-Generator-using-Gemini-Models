from pydantic import BaseModel, Field
from typing import Optional

class UserInput(BaseModel):
    user_id: int = Field(..., alias="user_id")
    username: str = Field(..., alias="username")
    age: int
    weight: float
    goal: str
    intensity: str

    class Config:
        populate_by_name = True

class WorkoutRequest(BaseModel):
    goal: str
    intensity: str

class FeedbackRequest(BaseModel):
    feedback: str