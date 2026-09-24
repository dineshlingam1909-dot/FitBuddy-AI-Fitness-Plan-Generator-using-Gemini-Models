from pydantic import BaseModel, Field, field_validator


class UserInput(BaseModel):

    user_id: str = Field(
        min_length=2,
        max_length=80
    )

    name: str = Field(
        min_length=2,
        max_length=120
    )

    age: int = Field(
        ge=13,
        le=100
    )

    weight: float = Field(
        gt=20,
        le=400
    )

    goal: str = Field(
        min_length=2,
        max_length=80
    )

    intensity: str

    @field_validator("intensity")
    @classmethod
    def validate_intensity(cls, value: str):

        value = value.lower().strip()

        allowed = {
            "low",
            "medium",
            "high"
        }

        if value not in allowed:
            raise ValueError(
                "Intensity must be low, medium, or high."
            )

        return value


class FeedbackRequest(BaseModel):

    user_id: str = Field(
        min_length=2,
        max_length=80
    )

    feedback: str = Field(
        min_length=3,
        max_length=1000
    )