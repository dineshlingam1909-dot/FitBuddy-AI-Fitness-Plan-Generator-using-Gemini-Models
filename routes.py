from fastapi import (
    APIRouter,
    Form,
    HTTPException,
    Request
)

from fastapi.templating import Jinja2Templates

from app.database import (
    save_user,
    get_user,
    save_plan,
    get_latest_plan,
    update_plan,
    get_all_users,
    get_all_plans
)

from app.schemas import (
    UserInput,
    FeedbackRequest
)

from app.ai.gemini_generator import (
    generate_workout_gemini
)

from app.ai.gemini_flash_generator import (
    generate_nutrition_tip_with_flash
)

from app.ai.updated_plan import (
    update_workout_plan
)


router = APIRouter()

templates = Jinja2Templates(
    directory="templates"
)


# =========================================
# HOME
# =========================================

@router.get("/")
def home(request: Request):

    return templates.TemplateResponse(
    request=request,
    name="index.html",
    context={
        "request": request
    }
)


# =========================================
# GENERATE WORKOUT
# =========================================

# =========================================
# GENERATE WORKOUT
# =========================================

@router.post("/generate-workout")
def generate_workout(
    request: Request,
    user_id: str = Form(...),
    name: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...)
):
    try:
        data = UserInput(
            user_id=user_id,
            name=name,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity
        )

        save_user(data)

        # Try Gemini first
        try:
            workout_plan = generate_workout_gemini(
                data.name,
                data.age,
                data.weight,
                data.goal,
                data.intensity
            )

        # If Gemini quota is exhausted, use local demo plan
        except Exception as exc:
            error_text = str(exc)

            if "429" in error_text or "quota" in error_text.lower():
                workout_plan = f"""
FITBUDDY 7-DAY WELLNESS PLAN
Demo / Local Fallback Mode

Hello {data.name}!

Day 1 - Full Body
Warm-up: 5 minutes
Main workout:
- Bodyweight squats: 3 sets
- Push-ups: 3 sets
- Glute bridges: 3 sets
- Plank: 3 rounds
Rest: 60 seconds between sets
Cool-down: 5 minutes

Day 2 - Upper Body
Warm-up: 5 minutes
Main workout:
- Incline push-ups: 3 sets
- Regular push-ups: 3 sets
- Shoulder taps: 3 sets
- Bird-dog: 3 sets
Cool-down: 5 minutes

Day 3 - Lower Body
Warm-up: 5 minutes
Main workout:
- Bodyweight squats: 3 sets
- Reverse lunges: 3 sets
- Glute bridges: 3 sets
- Calf raises: 3 sets
Cool-down: 5 minutes

Day 4 - Recovery
- Easy mobility exercises
- Light stretching
- Relaxation and recovery

Day 5 - Full Body
Warm-up: 5 minutes
Main workout:
- Squats: 3 sets
- Push-ups: 3 sets
- Mountain climbers: 3 rounds
- Plank: 3 rounds
Cool-down: 5 minutes

Day 6 - Core & Mobility
Warm-up: 5 minutes
Main workout:
- Dead bug: 3 sets
- Bird-dog: 3 sets
- Plank: 3 rounds
- Glute bridge: 3 sets
Cool-down: 5 minutes

Day 7 - Rest & Recovery
- Rest
- Gentle stretching
- Hydration
- Adequate sleep

Note:
This is a local demo fallback because the AI service
quota is temporarily unavailable.

Stop exercising if you experience pain or feel unwell.
"""
            else:
                raise

        # Temporary local nutrition tip
        nutrition_tip = (
            "Stay hydrated, eat balanced meals, "
            "and get enough sleep for recovery."
        )

        save_plan(
            data.user_id,
            workout_plan,
            nutrition_tip
        )

        plan = get_latest_plan(data.user_id)

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "request": request,
                "user": data,
                "plan": plan
            }
        )

    except Exception as exc:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "request": request,
                "error": str(exc)
            }
        )

# =========================================
# SUBMIT FEEDBACK
# =========================================

@router.post("/submit-feedback")
def submit_feedback(
    request: Request,

    user_id: str = Form(...),
    feedback: str = Form(...)
):

    try:

        feedback_data = FeedbackRequest(
            user_id=user_id,
            feedback=feedback
        )

        # Find user
        user = get_user(
            feedback_data.user_id
        )

        if not user:

            raise ValueError(
                "User ID not found."
            )

        # Find latest plan
        plan = get_latest_plan(
            feedback_data.user_id
        )

        if not plan:

            raise ValueError(
                "No workout plan found."
            )

        # Use updated plan if available
        current_plan = (
            plan["updated_plan"]
            or
            plan["original_plan"]
        )

        # Generate revised plan
        revised_plan = update_workout_plan(
            current_plan,
            feedback_data.feedback,
            user["goal"],
            user["intensity"]
        )

        # Save updated plan
        update_plan(
            plan["id"],
            revised_plan,
            feedback_data.feedback
        )

        # Get updated plan
        updated_plan = get_latest_plan(
            feedback_data.user_id
        )

        # Convert user database row to schema
        user_data = UserInput(
            user_id=user["user_id"],
            name=user["name"],
            age=user["age"],
            weight=user["weight"],
            goal=user["goal"],
            intensity=user["intensity"]
        )

        return templates.TemplateResponse(
    request=request,
    name="result.html",
    context={
        "request": request,
        "user": user_data,
        "plan": updated_plan,
        "message": "Workout plan updated successfully."
    }
)

    except Exception as exc:

        return templates.TemplateResponse(
    request=request,
    name="result.html",
    context={
        "request": request,
        "error": str(exc)
    }
)


# =========================================
# VIEW ALL USERS
# =========================================

@router.get("/view-all-users")
def view_all_users(
    request: Request
):

    users = get_all_users()

    plans = get_all_plans()

    latest_by_user = {}

    for plan in plans:

        if plan["user_id"] not in latest_by_user:

            latest_by_user[
                plan["user_id"]
            ] = plan

    return templates.TemplateResponse(
        request=request,
        name="all_users.html",
        context={
            "request": request,
            "users": users,
            "latest_by_user": latest_by_user
        }
    )

# =========================================
# API ENDPOINTS
# =========================================

@router.get("/api/health")
def health():

    return {
        "status": "ok",
        "service": "FitBuddy"
    }


# =========================================
# API - GENERATE WORKOUT
# =========================================

@router.post("/api/workouts")
def api_generate_workout(
    data: UserInput
):

    try:

        save_user(data)

        workout_plan = generate_workout_gemini(
            data.name,
            data.age,
            data.weight,
            data.goal,
            data.intensity
        )

        nutrition_tip = generate_nutrition_tip_with_flash(
            data.goal,
            data.intensity
        )

        plan_id = save_plan(
            data.user_id,
            workout_plan,
            nutrition_tip
        )

        return {
            "user_id": data.user_id,
            "plan_id": plan_id,
            "workout_plan": workout_plan,
            "nutrition_tip": nutrition_tip
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )


# =========================================
# API - FEEDBACK
# =========================================

@router.post("/api/feedback")
def api_feedback(
    data: FeedbackRequest
):

    user = get_user(
        data.user_id
    )

    plan = get_latest_plan(
        data.user_id
    )

    if not user or not plan:

        raise HTTPException(
            status_code=404,
            detail="User or workout plan not found."
        )

    try:

        current_plan = (
            plan["updated_plan"]
            or
            plan["original_plan"]
        )

        revised_plan = update_workout_plan(
            current_plan,
            data.feedback,
            user["goal"],
            user["intensity"]
        )

        update_plan(
            plan["id"],
            revised_plan,
            data.feedback
        )

        return {
            "plan_id": plan["id"],
            "updated_plan": revised_plan,
            "feedback": data.feedback
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )


# =========================================
# API - ALL USERS
# =========================================

@router.get("/api/users")
def api_users():

    users = get_all_users()

    return [
        {
            "user_id": user["user_id"],
            "name": user["name"],
            "age": user["age"],
            "weight": user["weight"],
            "goal": user["goal"],
            "intensity": user["intensity"]
        }
        for user in users
    ]