from app.ai.gemini_client import generate_text


def generate_workout_gemini(
    name,
    age,
    weight,
    goal,
    intensity
):

    prompt = f"""
You are FitBuddy, an AI fitness planning assistant.

Create a personalized 7-day general wellness workout plan.

User information:

Name: {name}
Age: {age}
Weight: {weight} kg
Fitness Goal: {goal}
Workout Intensity: {intensity}

Requirements:

1. Create exactly 7 days.
2. Clearly label Day 1 through Day 7.
3. Each day should contain:
   - Focus
   - Warm-up
   - Main workout
   - Sets/repetitions or duration
   - Rest guidance
   - Cool-down or recovery
4. Include at least one recovery/rest-oriented day.
5. Make the routine appropriate for the selected intensity.
6. Keep exercises practical and easy to understand.
7. Do not promise specific results.
8. Do not diagnose injuries or medical conditions.
9. Tell the user to stop if they experience pain or feel unwell.
10. Recommend qualified professional advice for medical concerns.

Return clean plain text.

Do not use JSON.
""".strip()

    return generate_text(
        prompt,
        purpose="workout"
    )