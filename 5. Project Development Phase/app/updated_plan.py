import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

def get_genai_client():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is not set.")
    return genai.Client(api_key=api_key)

def update_workout_plan(original_plan: str, user_feedback: str) -> str:
    """
    Use Gemini 1.5 Pro to update the workout plan based on user feedback.
    """
    prompt = f"""
You are a professional fitness trainer assistant.

Here's the original 7-day workout plan:
{original_plan}

User Feedback:
"{user_feedback}"

Based on the feedback, revise the relevant parts of the workout plan. Keep the format and rest of the plan unchanged if not needed.
"""
    try:
        client = get_genai_client()
        response = client.models.generate_content(
            model="gemini-1.5-pro",
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        return f"Error updating plan: {e}"