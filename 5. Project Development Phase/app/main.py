import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Mount Static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates location
templates = Jinja2Templates(directory="templates")

# Get API Key safely from .env file (Hardcoded key illa)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Latest supported Gemini model
model = genai.GenerativeModel("gemini-3.8-flash")

# In-memory storage for simple user feedback loop
user_data_store = {}


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="index.html"
    )


@app.post("/generate-workout", response_class=HTMLResponse)
async def generate_workout(
    request: Request,
    username: str = Form(...),
    user_id: int = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...)
):
    try:
        # SINGLE COMBINED PROMPT (Prevents 429 Quota Error)
        prompt = (
            f"Create a workout plan and nutrition tip for {username}.\n"
            f"Age: {age}, Weight: {weight}kg, Goal: {goal}, Intensity: {intensity}.\n\n"
            f"Respond EXACTLY in this format:\n"
            f"NUTRITION_TIP: <Write 1-2 sentences nutrition tip here>\n"
            f"WORKOUT_PLAN:\n<Write structured workout plan with bullet points here>"
        )
        
        response = model.generate_content(prompt)
        text = response.text

        # Separate the output into Nutrition Tip and Workout Plan
        if "NUTRITION_TIP:" in text and "WORKOUT_PLAN:" in text:
            parts = text.split("WORKOUT_PLAN:")
            nutrition_tip = parts[0].replace("NUTRITION_TIP:", "").strip()
            workout_plan = parts[1].strip()
        else:
            nutrition_tip = "Eat a balanced diet rich in protein and stay hydrated!"
            workout_plan = text

        user_data_store[user_id] = {
            "username": username,
            "age": age,
            "weight": weight,
            "goal": goal,
            "intensity": intensity,
            "workout_plan": workout_plan,
            "nutrition_tip": nutrition_tip
        }

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "username": username,
                "user_id": user_id,
                "workout_plan": workout_plan,
                "nutrition_tip": nutrition_tip,
                "message": "Workout plan generated successfully!"
            }
        )

    except Exception as e:
        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "username": username,
                "user_id": user_id,
                "workout_plan": f"Error generating plan: {str(e)}",
                "nutrition_tip": f"Error generating tip: {str(e)}",
                "message": None
            }
        )


@app.post("/update-workout", response_class=HTMLResponse)
async def update_workout(
    request: Request,
    user_id: int = Form(...),
    feedback: str = Form(...)
):
    user_info = user_data_store.get(user_id)
    
    if not user_info:
        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "username": "User",
                "user_id": user_id,
                "workout_plan": "Session expired or user not found. Please go back to Home.",
                "nutrition_tip": "N/A",
                "message": "User session not found."
            }
        )

    try:
        update_prompt = (
            f"Modify this existing workout plan: '{user_info['workout_plan']}' "
            f"based on the following user feedback: '{feedback}'. "
            f"Keep it well-structured and concise."
        )
        updated_response = model.generate_content(update_prompt)
        updated_plan = updated_response.text

        user_info['workout_plan'] = updated_plan

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "username": user_info['username'],
                "user_id": user_id,
                "workout_plan": updated_plan,
                "nutrition_tip": user_info['nutrition_tip'],
                "message": "Workout plan updated based on your feedback!"
            }
        )

    except Exception as e:
        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "username": user_info['username'],
                "user_id": user_id,
                "workout_plan": f"Error updating plan: {str(e)}",
                "nutrition_tip": user_info['nutrition_tip'],
                "message": None
            }
        )