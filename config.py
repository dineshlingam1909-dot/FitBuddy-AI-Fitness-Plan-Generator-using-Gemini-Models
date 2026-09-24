import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")

    workout_model: str = os.getenv(
        "GEMINI_WORKOUT_MODEL",
        "gemini-2.5-pro"
    )

    fast_model: str = os.getenv(
        "GEMINI_FAST_MODEL",
        "gemini-2.5-flash"
    )

    database_url: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./fitbuddy.db"
    )


settings = Settings()