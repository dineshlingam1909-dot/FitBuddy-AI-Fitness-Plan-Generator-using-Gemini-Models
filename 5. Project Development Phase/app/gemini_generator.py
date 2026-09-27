import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

def get_genai_client():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is not set.")
    return genai.Client(api_key=api_key)

def generate_workout_gemini(user_input: dict) -> str:
    prompt = f"""
You are a professional Fitness trainer.

Create a personalized, structured 7-day workout plan for someone with the goal of **{user_input['goal']}**, and prefers **{user_input['intensity']} intensity** workouts.

Each day must include:
- A warm-up (5-10 mins)
- Main workout (targeted exercises, sets & reps)
- Cooldown or recovery tip

Format:
Day 1:
Warm-up: ...
Main Workout: ...
Cooldown: ...
(Repeat for Day 2-7)
"""
    try:
        client = get_genai_client()
        response = client.models.generate_content(
            model="gemini-1.5-pro",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error: {e}"