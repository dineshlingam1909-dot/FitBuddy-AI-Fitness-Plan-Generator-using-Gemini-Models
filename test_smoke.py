from app.main import app


def test_app_metadata():

    assert app.title == "FitBuddy API"


def test_routes_exist():

    paths = {
        route.path
        for route in app.routes
    }

    assert "/" in paths

    assert "/generate-workout" in paths

    assert "/submit-feedback" in paths

    assert "/view-all-users" in paths

    assert "/api/health" in paths

    assert "/api/workouts" in paths

    assert "/api/feedback" in paths