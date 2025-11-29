from fastapi.testclient import TestClient
from weather_planner.app import app
from unittest.mock import patch

client = TestClient(app)

def test_actvities_endpoint():
    fake_weather = {
        "location": {"name": "Seattle"},
        "current": {
            "temp_f": 70,
            "wind_mph": 5,
            "condition": {"text": "Clear"}
        }
    }

    #Patch the get_weather() function used by /activities
    with patch("weather_planner.app.get_weather") as mock_get:
        mock_get.return_value= fake_weather

        response = client.post("/activities", json={"city": "Seattle"})
        assert response.status_code == 200

        data = response.json()
        assert "suggested_activity" in data
        assert "activity_message" in data
        assert data["city"] == "Seattle"