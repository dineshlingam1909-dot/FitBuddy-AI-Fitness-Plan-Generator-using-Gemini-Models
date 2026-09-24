from google import genai

from app.config import settings


_client = None


def get_client():

    global _client

    if not settings.gemini_api_key:

        raise RuntimeError(
            "GEMINI_API_KEY is missing. "
            "Please add your Gemini API key to the .env file."
        )

    if _client is None:

        _client = genai.Client(
            api_key=settings.gemini_api_key
        )

    return _client


def generate_text(
    prompt: str,
    purpose: str = "workout"
):

    client = get_client()

    if purpose == "fast":

        model = settings.fast_model

    else:

        model = settings.workout_model

    response = client.models.generate_content(
        model=model,
        contents=prompt
    )

    text = getattr(
        response,
        "text",
        None
    )

    if not text:

        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return text.strip()