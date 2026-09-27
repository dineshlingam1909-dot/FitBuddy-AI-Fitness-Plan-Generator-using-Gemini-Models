# FitBuddy AI

## Personalized Workout & Nutrition Plan Generator

FitBuddy AI is an AI-powered web application that generates personalized workout and nutrition plans based on the user's fitness information, fitness goals, and preferences.

## Features

- Personalized workout plan generation
- Personalized nutrition plan generation
- Fitness goal based recommendations
- FastAPI backend
- Jinja2 web interface
- Google Gemini AI integration
- User input validation
- Error handling

## Technology Stack

- Python
- FastAPI
- Jinja2
- Google Gemini
- HTML
- CSS
- JavaScript
- Uvicorn
- Python-dotenv

## How It Works

1. User opens the FitBuddy AI web application.
2. User enters fitness information and goals.
3. FastAPI receives the submitted information.
4. The application validates the user input.
5. A personalized AI prompt is created.
6. The prompt is sent to Google Gemini.
7. Gemini generates the workout and nutrition plan.
8. The backend processes the generated response.
9. Jinja2 displays the final plan on the web page.

## Project Structure

```text
FitBuddy-AI/
│
├── app/
│   ├── database.py
│   ├── gemini_flash_generator.py
│   ├── gemini_generator.py
│   ├── main.py
│   ├── nutrition.py
│   ├── routes.py
│   ├── schemas.py
│   └── updated_plan.py
│
├── static/
├── templates/
│
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
## 🎬 Project Demo Video
Watch the live demonstration of FitBuddy AI here: [FitBuddy AI Demo Video](https://drive.google.com/file/d/1Vd8kDwBLHwdAhosoShh2vGUn5CHFmsHW/view?usp=sharing)
