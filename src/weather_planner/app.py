import os
import requests

from quart import Quart, request, jsonify
from .suggestion import Suggestion

app = Quart(__name__)

api_key = os.getenv("WEATHER_API_KEY")

@app.post("/location")
async def post_location():
    # TODO: accept user locaton data and record it for use in weather lookups
    return

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

def get_weather(city):
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
    res = requests.get(url).json()
    return res

weather = get_weather("Seattle")
print(weather)

def find_activity(temp, wind, precipitation):
    """Returns the first valid activity based on the weather"""
    for a in activity_list():
        if (a.check_bound("temp", round(temp)) and a.check_bound("wind", round(wind)) and a.check_precipitation(precipitation)):
            return a
    return None

def find_outfit(temp, wind, precipitation):
    """Returns the first valid outfit based on the weather"""
    for o in outfit_list():
        if (o.check_bound("temp", round(temp)) and o.check_bound("wind", round(wind)) and o.check_precipitation(precipitation)):
            return o
    return None

def activity_list():
    """List of activities"""
    activities = [
        Suggestion("swimming","Why not go swimming?"),
        Suggestion("walk","It's great weather for a walk."),
        Suggestion("read","Get cozy with a book!"),
        Suggestion("snowman","Go build a snowman!")]

    activities[0].bounds = {
    "temp": (65,110),
    "wind": (0,10)}
    activities[1].bounds = {
    "temp": (30,64),
    "wind": (0,10)}
    activities[2].bounds = {
    "temp": (10,60),
    "wind": (0,30)}
    activities[3].bounds = {
    "temp": (-15,29),
    "wind": (0,10)}

    activities[0].precipitation = [
    "clear"]
    activities[1].precipitation = [
    "clear",
    "cloudy"]
    activities[2].precipitation = [
    "rain", "rainy"]
    activities[3].precipitation = [
    "snow", "snowy"]

    return activities
    

def outfit_list():
    """List of outfits"""
    outfits = [
        Suggestion("shorts","Perfect for shorts and a T-shirt!"),
        Suggestion("sweater","Better bring a sweater."),
        Suggestion("raincoat","Bring a raincoat!"),
        Suggestion("coat","You're gonna need a coat!")]

    outfits[0].bounds = {
    "temp": (65,110),
    "wind": (0,15)}
    outfits[1].bounds = {
    "temp": (30,64),
    "wind": (0,20)}
    outfits[2].bounds = {
    "temp": (10,60),
    "wind": (0,25)}
    outfits[3].bounds = {
    "temp": (-15,29),
    "wind": (0,30)}

    outfits[0].precipitation = [
    "clear",
    "cloudy"]
    outfits[1].precipitation = [
    "clear",
    "cloudy"]
    outfits[2].precipitation = [
    "rainy"]
    outfits[3].precipitation = [
    "clear",
    "cloudy",
    "snowy"]

    return outfits

def run() -> None:
    app.run()
