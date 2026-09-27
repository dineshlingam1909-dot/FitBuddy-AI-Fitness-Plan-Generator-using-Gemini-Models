import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

def get_genai_client():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is not set.")
    return genai.Client(api_key=api_key)

def generate_nutrition_tip_with_flash(goal: str) -> str:
    """
    Generate a nutrition or recovery tip using Gemini Flash based on the user's fitness goal.
    """
    prompt = (
        f"Give one clear, helpful nutrition or recovery tip for someone focused on '{goal}'. "
        "The tip should be practical, friendly, and easy to understand."
    )
    try:
        client = get_genai_client()
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        return f"Error generating tip: {str(e)}"