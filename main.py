from pathlib import Path

from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles

from app.database import init_db

from app.routes import router


BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_DIR = BASE_DIR / "static"


app = FastAPI(

    title="FitBuddy API",

    description=(
        "AI-powered personalized "
        "fitness plan generator"
    ),

    version="1.0.0"
)


app.mount(
    "/static",
    StaticFiles(
        directory=STATIC_DIR
    ),
    name="static"
)


app.include_router(
    router
)


@app.on_event("startup")
def startup():

    init_db()