from fastapi.testclient import TestClient
from weather_planner.app import app
from unittest.mock import patch

client = TestClient(app)

def test_forecast_endpoint():
    fake_weather = {
        "location": {"name": "Seattle"},
        "forecast": {"forecastday": []}
    }

    with patch("weather_planner.app.requests.get") as mock_get:
        mock_get.return_value.json.return_value = fake_weather

        response = client.get("/forecast?city=Seattle")
        assert response.status_code == 200

        data = response.json()
        assert "forecast" in data
        assert data["location"]["name"] == "Seattle"