from app.gemini_flash_generator import generate_nutrition_tip_with_flash

def get_goal_nutrition_tip(goal: str) -> str:
    """
    Helper function to wrap nutrition tip generation logic.
    """
    return generate_nutrition_tip_with_flash(goal)