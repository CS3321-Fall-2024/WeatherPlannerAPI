from quart import Quart, request, jsonify

app = Quart(__name__)

@app.get("/clothing")
async def get_clothing_suggestions():
    # TODO: get weather data and use it to look up clothing suggestions
    return

@app.get("/forecast")
async def get_forecast():
    # TODO: get forecast for the next 14 days
    return

@app.get("/activities")
async def get_activities():
    # TODO: get weather and suggest possible activities
    return

def run() -> None:
    app.run()
