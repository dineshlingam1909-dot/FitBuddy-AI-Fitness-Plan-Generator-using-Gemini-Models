import os
from fastapi import APIRouter, Request, Form, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.schemas import UserInput, WorkoutRequest, FeedbackRequest
from app.database import (
    save_user, save_plan, update_plan, 
    get_original_plan, get_user, SessionLocal, User, WorkoutPlan
)
from app.gemini_generator import generate_workout_gemini
from app.gemini_flash_generator import generate_nutrition_tip_with_flash
from app.updated_plan import update_workout_plan

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATE_DIR)

# --- WEB UI ROUTES ---

@router.get("/", response_class=HTMLResponse)
def home_page(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@router.post("/generate-workout", response_class=HTMLResponse)
async def generate_workout_ui(
    request: Request,
    username: str = Form(...),
    user_id: int = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...)
):
    # Save User to DB
    save_user(user_id=user_id, name=username, age=age, weight=weight, goal=goal, intensity=intensity)

    # Generate Plan & Tip
    user_input = {"goal": goal, "intensity": intensity}
    plan = generate_workout_gemini(user_input)
    nutrition_tip = generate_nutrition_tip_with_flash(goal)

    # Save initial plan to DB
    save_plan(user_id=user_id, plan=plan)

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "username": username,
            "user_id": user_id,
            "age": age,
            "weight": weight,
            "goal": goal,
            "intensity": intensity,
            "workout_plan": plan,
            "nutrition_tip": nutrition_tip,
            "message": None
        }
    )


@router.post("/submit-feedback", response_class=HTMLResponse)
async def submit_feedback_ui(
    request: Request,
    user_id: int = Form(...),
    feedback: str = Form(...)
):
    db_user = get_user(user_id)
    original_plan = get_original_plan(user_id)

    if not db_user or not original_plan:
        raise HTTPException(status_code=404, detail="User or original plan not found.")

    # Update Plan via AI
    updated_plan_text = update_workout_plan(original_plan, feedback)
    update_plan(user_id, updated_plan_text)
    
    # Get a fresh nutrition tip
    nutrition_tip = generate_nutrition_tip_with_flash(db_user.goal)

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "username": db_user.name,
            "user_id": db_user.id,
            "age": db_user.age,
            "weight": db_user.weight,
            "goal": db_user.goal,
            "intensity": db_user.intensity,
            "workout_plan": updated_plan_text,
            "nutrition_tip": nutrition_tip,
            "message": "Your plan has been updated based on your feedback!"
        }
    )

@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(request: Request):
    db = SessionLocal()
    try:
        users = db.query(User).all()
        user_data = []
        for user in users:
            plan = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user.id).first()
            user_data.append({
                "id": user.id,
                "name": user.name,
                "age": user.age,
                "weight": user.weight,
                "goal": user.goal,
                "intensity": user.intensity,
                "original_plan": plan.original_plan if plan else "N/A",
                "updated_plan": plan.updated_plan if (plan and plan.updated_plan) else "Not updated"
            })
        return templates.TemplateResponse(
            request=request,
            name="all_users.html",
            context={"users": user_data}
        )
    finally:
        db.close()


# --- RAW JSON API ENDPOINTS ---

@router.post("/generate-workout/gemini")
async def generate_gemini_workout_api(request: WorkoutRequest):
    try:
        result = generate_workout_gemini({"goal": request.goal, "intensity": request.intensity})
        return {"model": "gemini-pro", "workout_plan": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/nutrition-tip")
def get_flash_tip_api(goal: str):
    tip = generate_nutrition_tip_with_flash(goal)
    return {"goal": goal, "nutrition_tip": tip}


@router.post("/generate-plan")
def generate_plan_api(user_data: UserInput):
    try:
        save_user(
            user_id=user_data.user_id,
            name=user_data.username,
            age=user_data.age,
            weight=user_data.weight,
            goal=user_data.goal,
            intensity=user_data.intensity
        )
        plan = generate_workout_gemini({
            "goal": user_data.goal,
            "intensity": user_data.intensity
        })
        save_plan(user_data.user_id, plan)
        return {
            "message": "Workout plan generated and saved successfully!",
            "workout_plan": plan
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {str(e)}")


@router.post("/update-plan/{user_id}")
def update_user_plan_api(user_id: int, data: FeedbackRequest):
    original = get_original_plan(user_id)
    if not original:
        return {"error": "Original plan not found for this user."}
    updated = update_workout_plan(original, data.feedback)
    update_plan(user_id, updated)
    return {"updated_plan": updated}