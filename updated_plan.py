from app.ai.gemini_client import generate_text


def update_workout_plan(
    original_plan,
    feedback,
    goal,
    intensity
):

    prompt = f"""
You are FitBuddy.

The user already has a 7-day workout plan.

Fitness goal:
{goal}

Workout intensity:
{intensity}

User feedback:
{feedback}

Original workout plan:
{original_plan}

Task:

Create a complete revised 7-day workout plan.

Requirements:

1. Return Day 1 through Day 7.
2. Apply the user's feedback where appropriate.
3. Keep the workout balanced.
4. Include warm-up.
5. Include main workout.
6. Include recovery/cool-down.
7. Include at least one recovery/rest day.
8. Do not diagnose medical conditions.
9. Do not promise specific outcomes.
10. If requested changes could be unsafe, replace them with a safer general option.

Return clean plain text.
""".strip()

    return generate_text(
        prompt,
        purpose="workout"
    )