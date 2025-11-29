from fastapi.testclient import TestClient
from weather_planner.app import app
from unittest.mock import patch

client = TestClient(app)

def test_location_endpoint():
    fake_response = {
        "location": {
            "name": "Seattle",
            "region": "Washington",
            "tz_id": "America/Los_Angeles",
        }
    }

    #Patch the function get_location() uses internally: get_weather()
    with patch("weather_planner.app.requests.get") as mock_get:
        mock_get.return_value.json.return_value = fake_response

        response = client.get("/location?city=Seattle")

        assert response.status_code == 200
        body = response.json()

        assert "location" in body
        assert body["location"]["name"] == "Seattle"