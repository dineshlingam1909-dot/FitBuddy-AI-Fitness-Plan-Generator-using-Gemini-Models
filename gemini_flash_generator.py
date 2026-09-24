from app.ai.gemini_client import generate_text


def generate_nutrition_tip_with_flash(
    goal,
    intensity
):

    prompt = f"""
You are FitBuddy.

Give one concise nutrition or recovery tip.

Fitness goal:
{goal}

Workout intensity:
{intensity}

Requirements:

- Keep it practical.
- Focus on healthy food, hydration, sleep, or recovery.
- Keep it under 100 words.
- Avoid extreme dieting.
- Avoid medical claims.
- Avoid prescribing supplements.

Return only the tip.
""".strip()

    return generate_text(
        prompt,
        purpose="fast"
    )